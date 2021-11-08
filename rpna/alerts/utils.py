import random
import string

from django.conf import settings

import log
import phonenumbers
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client


def format_number(value: str) -> tuple[str, str]:
    try:
        parsed = phonenumbers.parse(value, "US")
    except phonenumbers.NumberParseException as e:
        return value, e.args[0]
    return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164), ""


def generate_code(user):
    code = "".join(random.choice(string.digits) for _ in range(6))
    user.set_password(code)
    user.save()
    return code


def send_text_message(number: str, message: str) -> bool:
    success = False
    if settings.TWILIO_ACCOUNT_SID:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        try:
            message = client.messages.create(
                to=number, from_=settings.TWILIO_NUMBER, body=message
            )
        except TwilioRestException as e:
            log.error(e)
        else:
            log.info(f"Sent text message (sid={message.sid})")  # type: ignore
            success = True
    else:
        log.error("Twilio credentials are not set")
    return success
