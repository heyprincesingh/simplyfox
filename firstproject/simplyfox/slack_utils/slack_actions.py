from simplyfox.slack_utils.slack_post_message import post_slack_block_message
from simplyfox.slack_utils.slack_view_publish import view_publish
from .slack_summary_text import handle_summary_creation, handle_summary_query


def button_days_selected(client, bot_token, user_id, data):
    channels_list = []
    days_selected = 0
    final_value = data.get("view")["state"]

    for key, value in final_value.get("values", {}).items():
        if "channelsList" in value:
            channels_list = value["channelsList"].get("selected_channels", [])
        if "daysSelect" in value and value["daysSelect"]["selected_option"] is not None:
            days_selected = value["daysSelect"]["selected_option"].get("value", {})

    if channels_list or days_selected:
        view_publish(
            client=client,
            user_id=user_id,
            block_id="app_home_days_selected",
            updated_data=[channels_list, days_selected],
        )

    return


def button_get_summary(client, bot_token, user_id, data):
    channels_list = []
    days_selected = 0
    final_value = data.get("view")["state"]

    for key, value in final_value.get("values", {}).items():
        if "channelsList" in value:
            channels_list = value["channelsList"].get("selected_channels", [])
        if "daysSelect" in value and value["daysSelect"]["selected_option"] is not None:
            days_selected = value["daysSelect"]["selected_option"].get("value", {})

    if channels_list or days_selected:
        handle_summary_creation(
            client=client,
            bot_token=bot_token,
            user_id=user_id,
            channels_list=channels_list,
            days_selected=days_selected,
        )


def button_save_summary(client, user_id, data):
    if "view" in data and "blocks" in data["view"]:
        data["view"]["blocks"] = data["view"]["blocks"][:-2]

        post_slack_block_message(
            client=client, receiver_id=user_id, block_message=data["view"]["blocks"]
        )


def fetch_user_query(client, user_id, conversation_data, user_query, blocks):
    if conversation_data != {} and user_query is not None:
        handle_summary_query(
            client=client,
            user_id=user_id,
            conversation_data=conversation_data,
            user_query=user_query,
            blocks=blocks,
        )
