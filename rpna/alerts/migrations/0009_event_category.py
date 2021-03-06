# Generated by Django 3.2.9 on 2021-11-06 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alerts", "0008_event_created_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="link",
        ),
        migrations.RemoveField(
            model_name="event",
            name="message",
        ),
        migrations.AddField(
            model_name="event",
            name="category",
            field=models.CharField(
                choices=[("N", "Neighborhood Update"), ("V", "Volunteer Opporunity")],
                default="N",
                max_length=1,
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="link_english",
            field=models.URLField(
                blank=True,
                help_text="Destination URL back to the main website.",
                null=True,
                verbose_name="Message (English)",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="message_english",
            field=models.CharField(
                default="",
                help_text="The text message content, not including the URL.",
                max_length=117,
                verbose_name="Message (English)",
            ),
            preserve_default=False,
        ),
    ]
