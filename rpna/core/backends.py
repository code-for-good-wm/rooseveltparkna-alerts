from django.conf import settings
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

import log
import requests


class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if user := super().authenticate(request, username, password, **kwargs):  # type: ignore
            return user

        if username.startswith("+"):
            return None

        data = {"username": username, "password": password}
        response = requests.post(settings.AUTH_URL, data)
        data = response.json()

        if response.status_code != 200:
            messages.error(request, data["message"])
            return None

        username = data["user_nicename"]
        email = data["user_email"]
        display_name = data["user_display_name"]
        first_name, last_name = display_name.rsplit(" ", 1)

        user, created = User.objects.update_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
            },
        )
        if created:
            log.info(f"New admin user: {user}")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
