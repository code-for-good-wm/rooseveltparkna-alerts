# pylint: disable=unused-argument

from django.contrib import admin, messages
from django.utils import timezone
from django.utils.html import format_html

from .models import Event
from .utils import format_number, send_text_message


def send_selected_events(modeladmin, request, queryset):
    count = 0
    event: Event
    for event in queryset:
        if event.test_number:
            send_text_message(event.test_number, event.content_english)
        if not event.sent:
            event.sent = True
            event.sent_at = timezone.now()
            event.save()
            count += 1
    messages.success(request, f"Scheduled alerts for {count} event(s).")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    search_fields = ["message", "link"]

    list_filter = ["category", "sent"]
    list_display = [
        "id",
        "category",
        "message_english",
        "_link_english",
        "message_spanish",
        "_link_spanish",
        "sent",
        "created_at",
    ]

    @staticmethod
    @admin.display(description="Link (English)")
    def _link_english(instance):
        if url := instance.link_english:
            return format_html(f'<a href="{url}" target="_blank">{url}</a>')
        return None

    @staticmethod
    @admin.display(description="Link (Spanish)")
    def _link_spanish(instance):
        if url := instance.link_spanish:
            return format_html(f'<a href="{url}" target="_blank">{url}</a>')
        return None

    actions = [send_selected_events]

    readonly_fields = ["created_by", "created_at"]

    def save_model(self, request, obj, form, change):
        obj.test_number = format_number(obj.test_number)[0]
        obj.created_by = request.user
        super().save_model(request, obj, form, change)
