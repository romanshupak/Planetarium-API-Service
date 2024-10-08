# Generated by Django 5.0.7 on 2024-08-06 17:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("planetarium", "0005_alter_astronomyshow_themes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="reservation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="planetarium.reservation",
            ),
        ),
    ]
