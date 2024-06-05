from slack_channel_summary.slack_utils.slack_get_functions import get_channel_conversation
from slack_channel_summary.utils.llm_model.langchain_main import langchain_generate_query_answer
from slack_channel_summary.slack_utils.slack_fetch_messages import fetch_messages_thread_replies
from slack_channel_summary.slack_utils.slack_view_publish import view_publish
from django.http import HttpResponse
import threading
import logging

logger = logging.getLogger(__name__)


def thread_http_response(response_status):
    return HttpResponse(status=response_status)


def thread_fetch_messages_thread_replies(
    client, bot_token, user_id, unread_channels_list, unread_channels_list_data
):
    try:
        final_updated_data = []
        for channel_id in unread_channels_list:
            channel_data = unread_channels_list_data[channel_id]
            start_date = channel_data["start_read_ts"]
            end_date = channel_data["end_read_ts"]

            # print(get_channel_conversation(client=client, channel_id=channel_id, start_date=start_date, end_date=end_date))
        #     thread_replies = fetch_messages_thread_replies(
        #         client=client,
        #         bot_token=bot_token,
        #         user_id=user_id,
        #         channels_list=[channel_id],
        #         start_date=start_date,
        #         end_date=end_date,
        #         query_asked="",
        #         isUnreadSummary=True
        #     )
        #     final_updated_data.append(thread_replies)
        # print(final_updated_data)
    #     published = view_publish(
    #         client=client,
    #         user_id=user_id,
    #         block_id="app_home_get_summary",
    #         updated_data=final_updated_data,
    #     )
    #     if published["ok"]:
    #         logger.info("Published summary for user_id: %s", user_id)
    #     else:
    #         logger.error(
    #             "Failed to publish summary for user_id: %s. Error: %s",
    #             user_id,
    #             published["error"],
    #             exc_info=True,
    #         )
    except Exception as e:
        logger.error(
            "Failed to publish thread replies for user_id: %s. Error: %s",
            user_id,
            e,
            exc_info=True,
        )


def thread_fetch_summary_query(client, user_id, conversation_data, user_query, blocks):
    try:
        queryData = langchain_generate_query_answer(
            user_id, conversation_data, user_query, token_counts=400
        )

        published = view_publish(
            client=client,
            user_id=user_id,
            block_id="app_home_query_answers",
            updated_data=[blocks, queryData],
        )
        if published["ok"]:
            logger.info("Published query for user_id: %s", user_id)
        else:
            logger.error(
                "Failed to publish query for user_id: %s. Error: %s",
                user_id,
                published["error"],
                exc_info=True,
            )

    except Exception as e:
        logger.error(
            "Failed to publish thread replies for user_id: %s. Error: %s",
            user_id,
            e,
            exc_info=True,
        )


def handle_unread_summary_creation(
    client, bot_token, user_id, unread_channels_list, unread_channels_list_data
):
    view_publish(
        client=client,
        user_id=user_id,
        block_id="app_home_summary_loading",
    )

    t1 = threading.Thread(target=thread_http_response, args=[200])
    t2 = threading.Thread(
        target=thread_fetch_messages_thread_replies,
        args=[
            client,
            bot_token,
            user_id,
            unread_channels_list,
            unread_channels_list_data,
        ],
    )
    t1.start()
    t2.start()


def handle_summary_query(client, user_id, conversation_data, user_query, blocks):
    t1 = threading.Thread(target=thread_http_response, args=[200])
    t2 = threading.Thread(
        target=thread_fetch_summary_query,
        args=[
            client,
            user_id,
            conversation_data,
            user_query,
            blocks,
        ],
    )
    t1.start()

    view_publish(
        client=client,
        user_id=user_id,
        block_id="replace_last_block_with_loading",
        updated_data=blocks,
    )

    t2.start()
