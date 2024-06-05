from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import threading
from django.conf import settings
from smtplib import SMTP
from django.http import HttpResponse
import markdown


def thread_http_response(response_status):
    return HttpResponse(status=response_status)


def thread_send_mail(to_email, subject, message):
    send_email(to_email, subject, message)


def send_email(to_email, subject, message):
    logger = logging.getLogger(__name__)
    try:
        server = SMTP(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT)
        server.connect(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(
            user=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD
        )

        multipart_msg = MIMEMultipart("alternative")
        multipart_msg["Subject"] = subject
        multipart_msg["From"] = f"slack_summary <{settings.EMAIL_HOST_USER}>"
        multipart_msg["To"] = to_email

        text = message
        html = markdown.markdown(text)

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        multipart_msg.attach(part1)
        multipart_msg.attach(part2)

        server.sendmail(settings.EMAIL_HOST_USER, to_email, multipart_msg.as_string())
        server.quit()

    except Exception as e:
        logger.error(
            "Failed to send email to %s. Error: %s", to_email, e, exc_info=True
        )


def trigger_send_mail_function(to_email, subject, message):
    t1 = threading.Thread(target=thread_http_response, args=[200])
    t2 = threading.Thread(target=thread_send_mail, args=[to_email, subject, message])

    t1.start()
    t2.start()
