import random
import string
from datetime import timedelta

from django.utils import timezone

import phonenumbers

from rpna.core.models import Profile

from .models import Event


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


def send_alerts() -> int:
    count = 0

    age = timezone.now() - timedelta(hours=1)
    for event in Event.objects.filter(sent_at__gte=age):
        for profile in Profile.objects.filter(alerted_at__lte=event.sent_at):
            if profile.alert(event):
                count += 1

    return count
