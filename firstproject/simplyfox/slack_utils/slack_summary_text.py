from simplyfox.generate_ai_summary import generate_ai_query_answer
from simplyfox.slack_utils.slack_view_publish import view_publish
from simplyfox.fetch_messages import fetch_messages_thread_replies
import threading
from django.http import HttpResponse


def thread_http_response(response_status):
    return HttpResponse(status=response_status)


def thread_fetch_messages_thread_replies(
    client, bot_token, user_id, channels_list, start_date, end_date, query_asked
):
    view_publish(
        client=client,
        user_id=user_id,
        block_id="app_home_get_summary",
        updated_data=fetch_messages_thread_replies(
            client, bot_token, user_id, channels_list, start_date, end_date, query_asked
        ),
    )


def thread_fetch_summary_query(client, user_id, conversation_data, user_query, blocks):
    answer = generate_ai_query_answer(
        conversationData=conversation_data, user_query=user_query
    )
    queryData = f"*Ques: {user_query}*\n*Ans:* {answer}"

    view_publish(
        client=client,
        user_id=user_id,
        block_id="app_home_query_answers",
        updated_data=[blocks, queryData],
    )


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
