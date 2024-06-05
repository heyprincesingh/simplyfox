from slack_summary.slack_utils.slack_unread_summary import handle_unread_summary_creation
from slack_summary.slack_utils.slack_get_functions import fetch_user_channels_list, get_channel_info
# from slack_summary.utils.db_utils import fetch_last_text_ts, update_channel_ts

def update_channel_unread_ts(data):
    team_id = data.get("team_id")
    channel_id = data.get("event", {}).get("channel")
    last_text_ts = data.get("event", {}).get("ts")
    # update_channel_ts(team_id=team_id, channel_id=channel_id, last_ts=last_text_ts)


def handle_unread_summary(client, bot_token, user_id, data):
    user_channel_list = fetch_user_channels_list(client=client, user_id=user_id)
    unread_channels_list = []
    unread_channels_list_data = {}
    # for channel in user_channel_list:
    #     user_last_read_ts = get_channel_info(client=client, channel_id=channel['id'])
    #     if user_last_read_ts["ok"]:
    #         last_message_ts = fetch_last_text_ts(team_id=data.get("user")['team_id'], channel_id=channel["id"])
    #         if last_message_ts and last_message_ts > user_last_read_ts["channel"]["last_read"]:
    #             unread_channels_list.append(channel["id"])
    #             unread_channels_list_data[channel["id"]] = {
    #                 'start_read_ts': user_last_read_ts["channel"]["last_read"],
    #                 'end_read_ts': last_message_ts
    #             }
    # handle_unread_summary_creation(
    #     client=client,
    #     bot_token=bot_token,
    #     user_id=user_id,
    #     unread_channels_list=unread_channels_list,
    #     unread_channels_list_data=unread_channels_list_data
    # )