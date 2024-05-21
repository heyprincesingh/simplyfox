def get_user_name(client, user_id):
    response = client.users_info(user=user_id)
    return response["user"]["profile"]["real_name"] if response["ok"] else user_id


def get_channel_name(client, channel_id):
    response = client.conversations_info(channel=channel_id)
    return response["channel"]["name"].capitalize() if response["ok"] else channel_id


def get_channel_conversation(client, channel_id, start_date, end_date):
    return client.conversations_history(channel=channel_id, oldest=start_date, latest=end_date)


def get_thread_conversations(client, channel_id, thread_timestamp):
    return client.conversations_replies(channel=channel_id, ts=thread_timestamp)

def get_user_info(client, user_id):
    return client.users_info(user=user_id)