from datetime import datetime
import json
import logging
import requests
from slack_summary.slack_utils.slack_blocks import slack_block
from slack_summary.slack_utils.slack_post_message import post_slash_error_message
from slack_summary.slack_utils.slack_fetch_messages import fetch_messages_thread_replies
from slack_summary.utils.day_functions import convert_date_string_to_unix, validate_date_format
import threading

logger = logging.getLogger(__name__)

def thread_http_response(response_url):
    message_payload = { 
        "response_type": "ephemeral",
        "blocks": slack_block('slash_loading_block')
    }

    headers = {"Content-Type": "application/json"}
    requests.post(response_url, headers=headers, data=json.dumps(message_payload))


def thread_fetch_summary_query(
    client, bot_token, user_id, channel_id, text_data, response_url
):
    try:
        start_date, end_date, query = slash_parse_date_query(text_data)
        updated_data = fetch_messages_thread_replies(
            client=client,
            bot_token=bot_token,
            user_id=user_id,
            channels_list=[channel_id],
            start_date=start_date,
            end_date=end_date,
            query_asked=query,
            isSlash=True,
        )

        message_payload = {
            "response_type": "ephemeral",
            "blocks": updated_data,
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(response_url, headers=headers, data=json.dumps(message_payload))
        
        if response.status_code == 200:
            logger.info("Published summary using slash command for user_id: %s", user_id)
        else:
            logger.error("Failed to publish summary using slash command for user_id: %s. Error: %s", user_id, response["error"], exc_info=True)
    except Exception as e:
        logger.error("Failed to publish thread replies for user_id: %s. Error: %s", user_id, e, exc_info=True)


def slash_summarize_query(client, bot_token, data):
    user_id = data.get("user_id", [None])[0]
    channel_name = data.get("channel_name", [None])[0]
    channel_id = data.get("channel_id", [None])[0]
    
    if response_url := data.get("response_url", [None])[0]:
        if channel_name == "directmessage":
            post_slash_error_message(
                response_url=response_url,
                error_message="🚨 This command is not available in direct messages.",
            ) 
        else:
            text = data.get("text", [None])[0]
            t1 = threading.Thread(target=thread_http_response, args=[response_url])
            t2 = threading.Thread(
                target=thread_fetch_summary_query,
                args=[client, bot_token, user_id, channel_id, text, response_url],
            )

            t1.start()
            t2.start()


def slash_parse_date_query(input_str):
    today_unix = convert_date_string_to_unix(datetime.now().strftime('%d%b%Y'))
    start_date = today_unix
    end_date = today_unix
    query = ""

    if input_str is None:
        return start_date, end_date, query
    parts = input_str.split()
    if len(parts) >= 1 and validate_date_format(parts[0]):
        start_date = convert_date_string_to_unix(parts[0])
        if len(parts) >= 2 and validate_date_format(parts[1]):
            end_date = convert_date_string_to_unix(parts[1])
            query = " ".join(parts[2:]) if len(parts) > 2 else ""
        else:
            query = " ".join(parts[1:]) if len(parts) > 1 else ""
    else:
        query = " ".join(parts) if len(parts) > 0 else ""

    return start_date, end_date, query
