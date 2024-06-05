from django.urls import path
from .views import SlackSummaryView, SlackEventsView, SlackUserInteractionView

urlpatterns = [
    path('slack_summary', SlackSummaryView.as_view(), name='slack_summary'),
    path('eventsubs', SlackEventsView.as_view(), name='slack_events'),
    path('userinteraction', SlackUserInteractionView.as_view(), name='user_interaction'),
]