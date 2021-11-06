from django.core.management.base import BaseCommand

from rpna.alerts.helpers import send_alerts
from rpna.core.helpers import expire_passwords


class Command(BaseCommand):
    help = "Send scheduled alerts to residents"

    def handle(self, **_options):
        count = send_alerts()
        self.stdout.write(f"Sent {count} alert(s)")

        count = expire_passwords()
        self.stdout.write(f"Expired {count} password(s)")
