from datetime import timedelta

from django.utils import timezone

from rpna.core.models import Profile

from .models import Event


def send_alerts() -> int:
    count = 0

    age = timezone.now() - timedelta(hours=1)
    for event in Event.objects.filter(sent_at__gte=age):
        for profile in Profile.objects.filter(
            valid=True, alerted_at__lte=event.sent_at
        ):
            if profile.alert(event):
                count += 1

    return count
