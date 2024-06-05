import json
from slack_summary.utils.llm_model.langchain_main import langchain_generate_query_answer, langchain_generate_summary
from slack_summary.slack_utils.slack_blocks_data_functions import format_data_into_blocks
from slack_summary import shared_data
from .slack_get_functions import (
    get_channel_conversation,
    get_thread_conversations,
    get_user_name,
)
from ..utils.day_functions import convert_date_to_unix, convert_unix_to_date


def fetch_messages_thread_replies(
    client, bot_token, user_id, channels_list, start_date, end_date, query_asked, isSlash=False, isUnreadSummary = False
):
    user_names_list = {}
    formatted_messages = {}

    for channel_id in channels_list:
        client.conversations_join(token=bot_token, channel=channel_id)

        conversations = get_channel_conversation(
            client=client,
            channel_id=channel_id,
            start_date=start_date if (isSlash or isUnreadSummary) else convert_date_to_unix(start_date),
            end_date=end_date if (isSlash or isUnreadSummary) else convert_date_to_unix(end_date)
        )
        messages = conversations["messages"]

        thread_ts_set = {
            message["thread_ts"] for message in messages if "thread_ts" in message
        }

        thread_replies_dict = {
            thread_ts: get_thread_conversations(
                client=client, channel_id=channel_id, thread_timestamp=thread_ts
            )["messages"][1:]
            for thread_ts in thread_ts_set
        }

        formatted_channel_messages = []
        for message in messages:
            if message.get("type") == "message" and "subtype" not in message:
                formatted_message = {
                    "user": message.get("user"),
                    "text": message.get("text"),
                    "timeStamp": convert_unix_to_date(message.get("ts")),
                    "thread_reply": [],
                }

                if message.get("user") in user_names_list:
                    formatted_message["user"] = user_names_list[message.get("user")]
                else:
                    user_name = (
                        get_user_name(client, message.get("user"))
                        if message.get("user") != user_id
                        else "me"
                    )
                    formatted_message["user"] = user_name
                    user_names_list[message.get("user")] = user_name

                if "thread_ts" in message:
                    thread_ts = message["thread_ts"]
                    formatted_message["thread_reply"] = [
                        {
                            "user": (
                                user_names_list[reply.get("user")]
                                if reply.get("user") in user_names_list
                                else (
                                    get_user_name(client, reply.get("user"))
                                    if reply.get("user") != user_id
                                    else "me"
                                )
                            ),
                            "text": reply.get("text"),
                            "thread_timeStamp": convert_unix_to_date(thread_ts),
                        }
                        for reply in thread_replies_dict[thread_ts]
                    ]

                formatted_channel_messages.append(formatted_message)

        formatted_channel_messages.reverse()

        shared_data.user_conversation_data[user_id] = {} if (isSlash or isUnreadSummary) else formatted_channel_messages
        
        if formatted_channel_messages:
            if query_asked:
                summarizedChannelMessages = langchain_generate_query_answer(user_id=user_id, conversation_data=formatted_channel_messages, user_query=query_asked, token_counts=400)
            else:
                summarizedChannelMessages = langchain_generate_summary(user_id=user_id, conversation_data=formatted_channel_messages, token_counts=6000)
        else:
            summarizedChannelMessages = "No conversations found till selected date in the channel!"

        formatted_messages[channel_id] = summarizedChannelMessages

    return format_data_into_blocks(data=formatted_messages, isSlash=isSlash)
