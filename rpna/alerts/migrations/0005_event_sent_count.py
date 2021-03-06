# Generated by Django 3.2.9 on 2021-11-06 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alerts", "0004_event_sent_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="sent_count",
            field=models.IntegerField(
                default=0, help_text="Number of residents who have received this alert."
            ),
        ),
    ]
