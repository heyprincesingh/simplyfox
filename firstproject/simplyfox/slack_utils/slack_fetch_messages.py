from simplyfox.slack_utils.slack_blocks_data_functions import format_data_into_blocks
from simplyfox import shared_data
from .slack_get_functions import (
    get_channel_conversation,
    get_thread_conversations,
    get_user_name,
)
from ..utils.generate_ai_summary import generate_ai_query_answer, generate_ai_summary
from ..utils.day_functions import convert_date_to_unix, convert_unix_to_date


def fetch_messages_thread_replies(
    client, bot_token, user_id, channels_list, start_date, end_date, query_asked
):
    user_names_list = {}
    formatted_messages = {}

    for channel_id in channels_list:
        client.conversations_join(token=bot_token, channel=channel_id)

        conversations = get_channel_conversation(
            client=client,
            channel_id=channel_id,
            start_date=convert_date_to_unix(start_date),
            end_date=convert_date_to_unix(end_date)
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
        
        shared_data.conversation_data[user_id] = formatted_channel_messages
        
        if formatted_channel_messages:
            if query_asked:
                summarizedChannelMessages = generate_ai_query_answer(conversationData=formatted_channel_messages, user_query=query_asked)
            else:
                summarizedChannelMessages = generate_ai_summary(formatted_channel_messages)
        else:
            summarizedChannelMessages = "No conversations found till selected date in the channel!"

        formatted_messages[channel_id] = summarizedChannelMessages

    return format_data_into_blocks(formatted_messages)
