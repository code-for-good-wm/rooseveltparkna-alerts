from datetime import timedelta

from django.utils import timezone

from .models import Profile


def expire_passwords() -> int:
    count = 0

    for profile in Profile.objects.filter(valid=None):
        age = timezone.now() - profile.joined_at
        if age > timedelta(minutes=5):
            profile.invalidate()
            count += 1

    return count
