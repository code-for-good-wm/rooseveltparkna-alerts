# pylint: disable=unused-argument

from django.contrib import admin

from .models import Profile

admin.site.index_title = "Home"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    search_fields = ["user__username"]

    list_filter = ["valid"]
    list_display = [
        "number",
        "joined_at",
        "valid",
        "alerted_at",
    ]
