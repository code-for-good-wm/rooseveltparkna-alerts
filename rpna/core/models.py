# mypy: ignore-errors


from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from rpna.alerts.models import Event

from .helpers import send_text_message


def normalize(name: str) -> str:
    return name.lower().translate({ord(c): None for c in "-_ "})


class CustomUser:
    @property
    def display_name(self) -> str:
        full_name = self.get_full_name()
        if full_name and normalize(full_name) != normalize(self.username):
            return f"{self.username} ({full_name})"
        return self.username

    @property
    def profile_name(self) -> str:
        return self.get_full_name() or self.username

    @property
    def short_name(self) -> str:
        return self.first_name or self.username

    @property
    def is_trackable(self) -> bool:
        return (
            self.is_authenticated
            and "@example.com" not in self.email
            and "admin" not in self.username
        )


for _name in dir(CustomUser):
    if not _name.startswith("_"):
        method = getattr(CustomUser, _name)
        User.add_to_class(_name, method)


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    joined_at = models.DateTimeField(
        default=timezone.now, help_text="Timestamp when user requested a login code."
    )
    alerted_at = models.DateTimeField(
        default=timezone.now, help_text="Timestamp when user was last sent an alert."
    )

    def __str__(self):
        return self.number

    @property
    def number(self) -> str:
        return self.user.username

    def alert(self, event: Event) -> bool:
        if send_text_message(self.number, event.content):
            self.alerted_at = timezone.now()
            self.save()
            event.sent_count += 1
            event.save()
            return True
        return False
