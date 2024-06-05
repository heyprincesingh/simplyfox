from slack_summary.slack_utils.slack_actions import (
    button_get_summary,
    button_get_unread_summary,
    button_mail_summary,
    button_save_summary,
    fetch_user_query,
)
from urllib.parse import unquote_plus
from django.http import HttpResponse
from slack_summary import shared_data
import slack
import json
import os
import logging

logger = logging.getLogger(__name__)

class SlackInteractionHandler:
    def __init__(self, request):
        self.request = request
        self.bot_token = os.getenv("SLACK_BOT_TOKEN")
        self.client = slack.WebClient(token=self.bot_token)
        self.payload = unquote_plus(self.request.body.decode("utf-8"))
        self.data = json.loads(self.payload.split("=")[1])
        self.user_id = self.data.get("user")["id"]
        
        self.logger = logging.getLogger(__name__)
        
        self.action_handlers = {
            "buttonGetSummary": self.button_get_summary,
            "unread_summarize" : self.button_get_unread_summary,
            "saveSummary": self.button_save_summary,
            "mailSummary": self.button_mail_summary,
            "questionAskedTextBox": self.fetch_user_query,
        }

    def handle_interactions(self):
        try:
            if "actions" in self.data:
                for action in self.data.get("actions"):
                    action_id = action.get("action_id")
                    if handler := self.action_handlers.get(action_id):
                        handler()
                    else:
                        return HttpResponse(status=200)
        except Exception as e:
            self.logger.error(f"Error handling Slack interactions: {e}", exc_info=True)

    def button_get_summary(self):
        try:
            button_get_summary( 
                client=self.client,
                bot_token=self.bot_token,
                user_id=self.user_id,
                data=self.data,
            )
        except Exception as e:
            self.logger.error(f"Error handling buttonGetSummary: {e}", exc_info=True)

    def button_save_summary(self):
        try:
            button_save_summary(client=self.client, user_id=self.user_id, data=self.data)
        except Exception as e:
            self.logger.error(f"Error handling saveSummary: {e}", exc_info=True)

    def button_mail_summary(self):
        try:
            button_mail_summary(client=self.client, user_id=self.user_id, data=self.data)
        except Exception as e:
            self.logger.error(f"Error handling mailSummary: {e}", exc_info=True)

    def fetch_user_query(self):
        try:
            fetch_user_query(
                client=self.client,
                user_id=self.user_id,
                conversation_data=shared_data.user_conversation_data[self.user_id],
                user_query=self.data["actions"][0]["value"],
                blocks=self.data["view"]["blocks"],
            )
        except Exception as e:
            self.logger.error(f"Error handling questionAskedTextBox: {e}", exc_info=True)
            
    def button_get_unread_summary(self):
        try:
            button_get_unread_summary( 
                client=self.client,
                bot_token=self.bot_token,
                user_id=self.user_id,
                data=self.data,
            )
        except Exception as e:
            self.logger.error(f"Error handling buttonGetSummary: {e}", exc_info=True)

    def execute(self):
        self.handle_interactions()