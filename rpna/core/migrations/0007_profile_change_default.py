# Generated by Django 3.2.9 on 2021-11-07 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_profile_fix_nulls"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="neighborhood_updates",
            field=models.BooleanField(
                default=True, verbose_name="Neighborhood Updates"
            ),
        ),
    ]
