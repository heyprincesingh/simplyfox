from slack_summary.slack_utils.slack_unread_functions import handle_unread_summary
from slack_summary.slack_utils.slack_blocks_data_functions import format_blocks_into_data
from slack_summary.utils.send_mail import trigger_send_mail_function
from slack_summary.slack_utils.slack_get_functions import get_user_info
from slack_summary.utils.day_functions import valid_start_end_date
from slack_summary.slack_utils.slack_block_functions import remove_save_me_and_text_input_block
from slack_summary.slack_utils.slack_post_message import post_slack_block_message
from .slack_summary_text import handle_summary_creation, handle_summary_query


def button_get_summary(client, bot_token, user_id, data):
    channels_list = []
    start_date = ""
    end_date = ""
    query_asked = ""
    final_value = data.get("view")["state"]

    for key, value in final_value.get("values", {}).items():
        if "channelsList" in value:
            channels_list = value["channelsList"].get("selected_channels", [])
        if "startDate" in value:
            start_date = value["startDate"].get("selected_date", "")
        if "endDate" in value:
            end_date = value["endDate"].get("selected_date", "")
        if "questionAsked" in value:
            query_asked = value["questionAsked"].get("value", "")

    if channels_list and valid_start_end_date(start_date, end_date):
        handle_summary_creation(
            client=client,
            bot_token=bot_token,
            user_id=user_id,
            channels_list=channels_list,
            start_date=start_date,
            end_date=end_date,
            query_asked=query_asked,
        )
        

def button_get_unread_summary(client, bot_token, user_id, data):
    handle_unread_summary(client=client, bot_token=bot_token, user_id=user_id, data=data)


def button_save_summary(client, user_id, data):
    if "view" in data and "blocks" in data["view"]:
        data["view"]["blocks"] = remove_save_me_and_text_input_block(
            data["view"]["blocks"]
        )
        post_slack_block_message(
            client=client, receiver_id=user_id, block_message=data["view"]["blocks"]
        )


def button_mail_summary(client, user_id, data):
    user_info = get_user_info(client=client, user_id=user_id)
    if user_email := user_info["user"]["profile"]["email"]:
        trigger_send_mail_function(
            to_email=user_email,
            subject="Your Summary - slack_summary 🦊",
            message=format_blocks_into_data(client=client, block_data=data),
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
