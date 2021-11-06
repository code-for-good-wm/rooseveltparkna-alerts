# pylint: disable=unused-argument

from django.contrib import admin, messages
from django.utils import timezone
from django.utils.html import format_html

from rpna.core.helpers import send_text_message

from .helpers import format_number
from .models import Event


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

    @staticmethod
    @admin.display(description="URL (English)")
    def _url_english(instance):
        url = instance.url_english
        return format_html(f'<a href="{url}" target="_blank">{url}</a>')

    @staticmethod
    @admin.display(description="URL (Spanish)")
    def _url_spanish(instance):
        url = instance.url_spanish
        return format_html(f'<a href="{url}" target="_blank">{url}</a>')

    actions = [send_selected_events]

    readonly_fields = [
        "_url_english",
        "_url_spanish",
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
