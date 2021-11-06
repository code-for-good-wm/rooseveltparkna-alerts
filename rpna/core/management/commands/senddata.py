# pylint: disable=no-self-use

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

import log

from rpna.alerts.helpers import send_alerts
from rpna.core.models import Profile


class Command(BaseCommand):
    help = "Send scheduled alerts to residents"

    def handle(self, **_options):
        count = send_alerts()
        log.info(f"Sent {count} alert(s)")

        count = self.expire_passwords()
        log.info(f"Expired {count} password(s)")

    def expire_passwords(self) -> int:
        count = 0

        for profile in Profile.objects.filter(valid=None):
            age = timezone.now() - profile.joined_at
            if age > timedelta(minutes=5):
                profile.invalidate()
                count += 1

        return count
