# pylint: disable=unused-argument

from django.contrib import admin, messages
from django.utils import timezone

from .models import Event


def send_selected_events(modeladmin, request, queryset):
    count = 0
    event: Event
    for event in queryset:
        if not event.sent:
            event.sent = True
            event.sent_at = timezone.now()
            event.save()
            count += 1
    messages.success(request, f"Scheduled alerts for {count} event(s).")


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
        "sent_at",
        "sent_count",
    ]

    actions = [send_selected_events]

    readonly_fields = ["content", "sent"]
