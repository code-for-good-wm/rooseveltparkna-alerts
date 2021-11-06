# pylint: disable=unused-import

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Category(models.TextChoices):
    NEIGHBORHOOD_UPDATE = "n", _("Neighborhood Update")
    VOLUNTEER_OPPORTUNITY = "v", _("Volunteer Opporunity")


class Event(models.Model):
    category = models.CharField(max_length=1, choices=Category.choices)
    message_english = models.CharField(
        max_length=settings.SMS_MAX_LENGTH,
        verbose_name="Message (English)",
        help_text="The text message content, not including the URL.",
    )
    message_spanish = models.CharField(
        max_length=settings.SMS_MAX_LENGTH,
        verbose_name="Message (Spanish)",
        help_text="The text message content, not including the URL.",
    )
    link_english = models.URLField(
        verbose_name="Link (English)",
        null=True,
        blank=True,
        help_text="Destination URL back to the main website.",
    )
    link_spanish = models.URLField(
        verbose_name="Link (Spanish)",
        null=True,
        blank=True,
        help_text="Destination URL back to the main website.",
    )

    test_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Mobile number to send a test message.",
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        help_text="The date this event was first drafted.",
    )
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
        help_text="The organizer who drafted this alert.",
    )

    sent = models.BooleanField(
        default=False,
        editable=False,
        help_text="Indicates alerts has been scheduled to be sent.",
    )
    sent_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        help_text="The date alerts were scheduled to be sent.",
    )
    sent_count = models.IntegerField(
        default=0,
        editable=False,
        help_text="Number of residents who have received this alert.",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Alert {self.pk}"

    @property
    def url_english(self) -> str:
        return f"{settings.BASE_URL}/en/{self.pk or '#'}"

    @property
    def url_spanish(self) -> str:
        return f"{settings.BASE_URL}/es/{self.pk or '#'}"

    @property
    def content_english(self) -> str:
        return f"{self.message_english}\n\n{self.url_english}"

    @property
    def content_spanish(self) -> str:
        return f"{self.message_spanish}\n\n{self.url_spanish}"

    def clean(self):
        count = bool(self.link_english) + bool(self.link_spanish)
        if count == 1:
            raise ValidationError("A link is required for all languages.")
