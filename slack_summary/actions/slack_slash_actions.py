from slack_summary.slack_utils.slack_slash_functions import slash_summarize_query
from django.http import HttpResponse
from urllib.parse import parse_qs
import logging
import slack
import os

class SlackSlashActions:
    def __init__(self, request):
        self.request = request
        self.logger = logging.getLogger(__name__)
        
    def slash_summarize_query(self):
        try:
            parsed_data = parse_qs(self.request.body.decode("utf-8"))
            bot_token = os.getenv("SLACK_BOT_TOKEN")
            client = slack.WebClient(token=bot_token)
            slash_summarize_query(client=client, bot_token=bot_token, data=parsed_data)
            return HttpResponse(status=200)
        except Exception as e:
            self.logger.error(f"Error processing slash command for summarizing query: {e}", exc_info=True)
            return HttpResponse(status=500)

    def execute(self):
        return self.slash_summarize_query()