import random
import string
from datetime import timedelta

from django.utils import timezone

from rpna.core.models import Profile

from .models import Event


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
