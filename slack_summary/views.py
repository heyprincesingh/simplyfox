from slack_summary.actions.slack_interaction_actions import SlackInteractionHandler
from slack_summary.actions.slack_events_actions import SlackEventsHandler
from slack_summary.actions.slack_slash_actions import SlackSlashActions
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from dotenv import load_dotenv
from django.views import View

load_dotenv()

@method_decorator(csrf_exempt, name='dispatch')
class SlackSummaryView(View):
    def post(self, request):
        handler = SlackSlashActions(request)
        return handler.execute() 

@method_decorator(csrf_exempt, name='dispatch')
class SlackUserInteractionView(View):
    def post(self, request):
        action_handler = SlackInteractionHandler(request)
        action_handler.execute()
        return HttpResponse(status=200)

@method_decorator(csrf_exempt, name='dispatch')
class SlackEventsView(View):
    def post(self, request):
        handler = SlackEventsHandler(request)
        return handler.execute()
