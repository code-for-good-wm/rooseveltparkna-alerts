# mypy: ignore-errors


from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

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


class Language(models.TextChoices):
    ENGLISH = "en", _("English")
    SPANISH = "es", _("Spanish")


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    language = models.CharField(max_length=2, choices=Language.choices)
    neighborhood_updates = models.BooleanField(_("Neighborhood Updates"))
    volunteer_opportunities = models.BooleanField(_("Volunteer Opportunities"))

    joined_at = models.DateTimeField(
        default=timezone.now, help_text="Timestamp when user requested a login code."
    )
    valid = models.BooleanField(
        null=True,
        default=None,
        help_text="Indicates a user has entered a valid login code.",
    )
    alerted_at = models.DateTimeField(
        default=timezone.now, help_text="Timestamp when user was last sent an alert."
    )

    def __str__(self):
        return self.number

    @property
    def number(self) -> str:
        return self.user.username

    def invalidate(self):
        if not self.user.is_staff:
            password = User.objects.make_random_password()
            self.user.set_password(password)
        self.valid = False
        self.save()

    def alert(self, event: Event) -> bool:
        if self.language == Language.SPANISH:
            content = event.content_spanish
        else:
            content = event.content_english

        if send_text_message(self.number, content):
            self.alerted_at = timezone.now()
            self.save()
            event.sent_count += 1
            event.save()
            return True

        return False

    def clean(self):
        if not (self.neighborhood_updates or self.volunteer_opportunities):
            raise ValidationError(_("Please select at least one type of alert."))
