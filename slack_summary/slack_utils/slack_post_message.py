import json
import requests


def post_slack_text_message(client, receiver_id, text_message):
    return client.chat_postMessage(
        channel=receiver_id,
        text=text_message,
    )


def update_slack_text_message(client, receiver_id, ts, text_message):
    return client.chat_update(
        channel=receiver_id,
        text=text_message,
        ts=ts,
    )


def post_slack_block_message(client, receiver_id, block_message):
    return client.chat_postMessage(
        blocks=block_message,
        channel=receiver_id,
        text=" ",
    )


def update_slack_block_message(client, receiver_id, ts, block_message):
    return client.chat_update(
        channel=receiver_id,
        blocks=block_message,
        ts=ts,
        text=" ",
    )
    
    
def post_slash_error_message(response_url, error_message):
    message_payload = {
        "response_type": "ephemeral",
        "text": error_message,
    }

    headers = {"Content-Type": "application/json"}
    requests.post(
        response_url, headers=headers, data=json.dumps(message_payload)
    )
