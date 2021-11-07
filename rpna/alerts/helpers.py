from datetime import timedelta

from django.utils import timezone

from rpna.core.models import Profile

from .models import Category, Event


def send_alerts() -> int:
    count = 0

    age = timezone.now() - timedelta(hours=1)
    for event in Event.objects.filter(sent_at__gte=age):

        options = {"valid": True, "alerted_at__lte": event.sent_at}
        if event.category == Category.NEIGHBORHOOD_UPDATE:
            options["neighborhood_updates"] = True
        elif event.category == Category.VOLUNTEER_OPPORTUNITY:
            options["volunteer_opportunities"] = True

        for profile in Profile.objects.filter(**options):
            if profile.alert(event):
                count += 1

    return count
