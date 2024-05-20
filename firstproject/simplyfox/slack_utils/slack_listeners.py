from simplyfox import shared_data
from .slack_view_publish import view_publish
from slack.errors import SlackApiError
from dotenv import load_dotenv
import slack
import ssl
import json
import os

ssl._create_default_https_context = ssl._create_unverified_context

def home_event(body):
    bot_token = os.getenv("SLACK_BOT_TOKEN")
    client = slack.WebClient(token=bot_token)
    event_body = body["event"]["type"]
    if event_body == "app_home_opened":
        shared_data.conversation_data[body["event"]["user"]] = {}
        view_publish(
            client=client,
            user_id=body["event"]["user"],
            block_id="app_home_opened",
        )
    return


def extract_data(request):
    body = json.loads(request.POST["payload"])
    views = body["view"]
    channels_list = None
    days_selected = None
    if "state" in views:
        state = views["state"]
        if "values" in state:
            values = state["values"]
            channels_found = 0
            days_found = 0
            for key, value in values.items():
                if channels_found < 1 and "channelsList" in value:
                    channels_list = value["channelsList"]["selected_channels"]
                    channels_found += 1
                elif days_found < 1 and "daysSelect" in value:
                    days_selected = value["daysSelect"]["selected_option"]["value"]
                    days_found += 1

                if channels_found >= 1 and days_found >= 1:
                    break

    return (channels_list, days_selected)
