from django.urls import path
from . import views

urlpatterns = [
    path('eventsubs', views.slack_events, name='slack_events'),
    path('userinteraction', views.user_interaction, name='getSummary'),
]