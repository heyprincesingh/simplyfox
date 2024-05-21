from simplyfox import shared_data
from .slack_utils.slack_actions import (
    button_get_summary,
    button_mail_summary,
    button_save_summary,
    fetch_user_query,
)
from django.views.decorators.csrf import csrf_exempt
from .slack_utils.slack_listeners import home_event
from django.http import HttpResponse, JsonResponse
from urllib.parse import unquote_plus
from dotenv import load_dotenv
import slack
import json
import os

load_dotenv()


@csrf_exempt
def user_interaction(request):
    bot_token = os.getenv("SLACK_BOT_TOKEN")
    client = slack.WebClient(token=bot_token)
    if request.method == "POST":
        payload = unquote_plus(request.body.decode("utf-8"))
        json_data = json.loads(payload.split("=")[1])
        user_id = json_data.get("user")["id"]
        if "actions" in json_data:
            # if "actions" is "getSummary" in json_data
            if any(
                (
                    action.get("action_id") == "buttonGetSummary"
                    for action in json_data.get("actions")
                )
            ):
                button_get_summary(
                    client=client, bot_token=bot_token, user_id=user_id, data=json_data
                )

            # if "actions" is "saveSummary/mailSummary" in json_data
            elif any(
                (
                    action.get("action_id") == "saveSummary"
                    for action in json_data.get("actions")
                )
            ):
                button_save_summary(client=client, user_id=user_id, data=json_data)

            elif any(
                (
                    action.get("action_id") == "mailSummary"
                    for action in json_data.get("actions")
                )
            ):
                button_mail_summary(client=client, user_id=user_id, data=json_data)
            
            # if "actions" is "questionAskedTextBox" in json_data
            elif any(
                (
                    action.get("action_id") == "questionAskedTextBox"
                    for action in json_data.get("actions")
                )
            ):
                fetch_user_query(
                    client=client,
                    user_id=user_id,
                    conversation_data=shared_data.conversation_data[user_id],
                    user_query=json_data["actions"][0]["value"],
                    blocks=json_data["view"]["blocks"],
                )

    return HttpResponse(status=200)


@csrf_exempt
def slack_events(request):
    body = json.loads(request.body.decode("utf-8"))
    if body.get("type") == "url_verification" and "challenge" in body:
        challenge = body["challenge"]
        return JsonResponse({"challenge": challenge})
    elif body.get("type") == "event_callback":
        if body.get("event")["type"] == "message":
            return HttpResponse()
        home_event(body)
    return HttpResponse(status="200")
