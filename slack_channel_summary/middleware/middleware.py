import time
import hmac
import hashlib
import logging
from django.conf import settings
from django.http import JsonResponse


class SlackValidate:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        try:
            timestamp = request.headers.get("X-Slack-Request-Timestamp")
            slack_signature = request.headers.get("X-Slack-Signature")

            if not timestamp or not slack_signature:
                self.logger.warning("Missing Slack headers.")
                return JsonResponse({"error": "Missing Slack headers"}, status=400)

            if abs(time.time() - int(timestamp)) > 60 * 5:
                self.logger.warning("Request out of date.")
                return JsonResponse({"error": "Request out of date"}, status=400)

            sig_basestring = f"v0:{timestamp}:{request.body.decode('utf-8')}"
            local_signature = (
                "v0="
                + hmac.new(
                    settings.SLACK_SIGNING_SECRET.encode("utf-8"),
                    sig_basestring.encode("utf-8"),
                    hashlib.sha256,
                ).hexdigest()
            )

            if not hmac.compare_digest(local_signature, slack_signature):
                self.logger.error("Invalid signature.")
                return JsonResponse({"error": "Invalid signature"}, status=400)

            return self.get_response(request)
        
        except Exception as e:
            self.logger.error(f"Error during Slack request verification: {e}", exc_info=True)
            return JsonResponse({"error": "Internal server error"}, status=500)