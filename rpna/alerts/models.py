# pylint: disable=unused-import

from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):

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
