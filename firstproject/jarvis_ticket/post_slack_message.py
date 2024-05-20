def post_slack_text_message(client, receiver_id, text_message):
    return client.chat_postMessage(
        channel=receiver_id,
        text=text_message,
    )