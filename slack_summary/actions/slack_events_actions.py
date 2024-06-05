from slack_summary.slack_utils.slack_unread_functions import update_channel_unread_ts
from slack_summary.slack_utils.slack_listeners import home_event
from django.http import HttpResponse, JsonResponse
import logging
import json
logger = logging.getLogger(__name__)


class SlackEventsHandler:
    def __init__(self, request):
        self.request = request
        self.logger = logging.getLogger(__name__)

    def events_actions(self):
        try:
            body = json.loads(self.request.body.decode("utf-8"))
            if body.get("type") == "url_verification" and "challenge" in body:
                challenge = body["challenge"]
                return JsonResponse({"challenge": challenge})
            elif body.get("type") == "event_callback":
                if body.get("event", {}).get("type") == "message":
                    update_channel_unread_ts(data=body)
                    return HttpResponse(status=200)
                elif body.get("event", {}).get("type") == "app_home_opened":
                    home_event(body)
            return HttpResponse(status=200)
        except Exception as e:
            self.logger.error(f"Error processing Slack events: {e}", exc_info=True)
            return HttpResponse(status=500)

    def execute(self):
        return self.events_actions()
