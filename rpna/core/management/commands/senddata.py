from django.core.management.base import BaseCommand

import log

from rpna.alerts.helpers import send_alerts
from rpna.core.helpers import expire_passwords


class Command(BaseCommand):
    help = "Send scheduled alerts to residents"

    def handle(self, **_options):
        count = send_alerts()
        log.info(f"Sent {count} alert(s)")

        count = expire_passwords()
        log.info(f"Expired {count} password(s)")
