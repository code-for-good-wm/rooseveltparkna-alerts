# pylint: disable=unused-argument

from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    search_fields = ["message", "link"]

    list_filter = ["sent"]
    list_display = [
        "id",
        "url",
        "message",
        "link",
        "created_by",
        "sent",
    ]

    # TODO: Add admin action to send alerts
    # actions = [sent_alert]

    readonly_fields = ["content", "sent"]
