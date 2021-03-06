# Generated by Django 3.2.9 on 2021-11-06 15:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("alerts", "0005_event_sent_count"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                help_text="The organizer who drafted this alert.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="sent_at",
            field=models.DateTimeField(
                blank=True,
                editable=False,
                help_text="The date alerts were scheduled to be sent.",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="sent_count",
            field=models.IntegerField(
                default=0,
                editable=False,
                help_text="Number of residents who have received this alert.",
            ),
        ),
    ]
