# pylint: disable=unused-import

from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):

    sent = models.BooleanField(
        default=False,
        editable=False,
        help_text="Indicates alerts has been scheduled to be sent.",
    )
