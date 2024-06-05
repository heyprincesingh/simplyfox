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
    client, bot_token, user_id, channels_list, start_date, end_date, query_asked
):
    try:
    
        updated_data = fetch_messages_thread_replies(
            client, bot_token, user_id, channels_list, start_date, end_date, query_asked
        )

        published = view_publish(
            client=client,
            user_id=user_id,
            block_id="app_home_get_summary",
            updated_data=updated_data,
        )
        if published["ok"]:
            logger.info("Published summary for user_id: %s", user_id)
        else:
            logger.error("Failed to publish summary for user_id: %s. Error: %s", user_id, published["error"], exc_info=True)
    except Exception as e:
        logger.error("Failed to publish thread replies for user_id: %s. Error: %s", user_id, e, exc_info=True)


def thread_fetch_summary_query(client, user_id, conversation_data, user_query, blocks):
    try:
        queryData = langchain_generate_query_answer(user_id, conversation_data, user_query, token_counts=400)

        published = view_publish(
            client=client,
            user_id=user_id,
            block_id="app_home_query_answers",
            updated_data=[blocks, queryData],
        )
        if published["ok"]:
            logger.info("Published query for user_id: %s", user_id)
        else:
            logger.error("Failed to publish query for user_id: %s. Error: %s", user_id, published["error"], exc_info=True)
    
    except Exception as e:
        logger.error("Failed to publish thread replies for user_id: %s. Error: %s", user_id, e, exc_info=True)


def handle_summary_creation(
    client, bot_token, user_id, channels_list, start_date, end_date, query_asked
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
            channels_list,
            start_date,
            end_date,
            query_asked
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
