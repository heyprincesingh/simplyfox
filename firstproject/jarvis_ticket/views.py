from .post_slack_message import post_slack_text_message
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
from dotenv import load_dotenv
from datetime import datetime
import slack
import ssl
import os


load_dotenv()


@csrf_exempt
def home(request):
    return render(request, "home.html")


@csrf_exempt
def create_token(request):
    botToken = os.getenv("SLACK_BOT_TOKEN")
    client = slack.WebClient(token=botToken)
    ssl._create_default_https_context = ssl._create_unverified_context
    user_id = request.GET.get("userID")
    user_issue = request.GET.get("issue")
    date_Time = datetime.now()
    text_message = f'Ticket has been created 📩\n📝Issue: {user_issue}\n🕗 Time: {date_Time.strftime("%d/%m/%Y %H:%M:%S")}'
    response = post_slack_text_message(client, user_id, text_message)
    return HttpResponse(status=200) if response["ok"] else HttpResponse(status=400)
