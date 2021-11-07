# pylint: disable=unused-argument

from django.contrib import admin
from django.contrib.sites.models import Site

from allauth.account.models import EmailAddress

from .models import Profile

admin.site.index_title = "Home"

admin.site.unregister(EmailAddress)
admin.site.unregister(Site)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    search_fields = ["user__username"]

    list_filter = [
        "valid",
        "language",
        "neighborhood_updates",
        "volunteer_opportunities",
    ]
    list_display = [
        "number",
        "joined_at",
        "valid",
        "language",
        "neighborhood_updates",
        "volunteer_opportunities",
        "alerted_at",
        "received_count",
        "updated_at",
    ]

    ordering = ["-updated_at"]
