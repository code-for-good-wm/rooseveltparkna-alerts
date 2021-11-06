from django.conf import settings

import log
from twilio.rest import Client


def build_url(path: str) -> str:
    assert settings.BASE_URL
    assert path.startswith("/")
    return settings.BASE_URL + path


def allow_debug(request) -> bool:
    if not settings.ALLOW_DEBUG:
        return False
    if request.GET.get("debug") == "false":
        return False
    if request.GET.get("debug"):
        return True
    return settings.DEBUG


def send_text_message(number: str, message: str):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        to=number, from_=settings.TWILIO_NUMBER, body=message
    )
    log.info(f"Sent text message: {message}")
