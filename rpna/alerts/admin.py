# pylint: disable=unused-argument

from django.contrib import admin, messages
from django.utils import timezone

from rpna.core.helpers import send_text_message

from .helpers import format_number
from .models import Event


def send_selected_events(modeladmin, request, queryset):
    count = 0
    event: Event
    for event in queryset:
        if event.test_number:
            send_text_message(event.test_number, event.content)
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
        "created_at",
        "sent",
        "sent_at",
        "sent_count",
    ]

    actions = [send_selected_events]

    readonly_fields = [
        "created_by",
        "created_at",
        "sent",
        "sent_at",
        "sent_count",
    ]

    def save_model(self, request, obj, form, change):
        obj.test_number = format_number(obj.test_number)[0]
        obj.created_by = request.user
        super().save_model(request, obj, form, change)
