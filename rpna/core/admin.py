# pylint: disable=unused-argument

from django.contrib import admin

from .models import Profile

admin.site.index_title = "Home"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = [
        "number",
        "joined_at",
        "alerted_at",
    ]
