# pylint: disable=unused-import

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):

    message = models.CharField(
        max_length=settings.SMS_MAX_LENGTH,
        help_text="The text message content, not including the URL.",
    )
    link = models.URLField(
        null=True, blank=True, help_text="Destination URL back to the main website."
    )

    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="The organizer who drafted this alert.",
    )

    sent = models.BooleanField(
        default=False,
        editable=False,
        help_text="Indicates alerts has been scheduled to be sent.",
    )

    @property
    def url(self) -> str:
        return f"{settings.BASE_URL}/-/{self.pk}"

    @property
    def content(self) -> str:
        return f"{self.message}\n\n{self.url}"
