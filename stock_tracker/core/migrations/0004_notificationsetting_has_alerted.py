# Generated by Django 4.2.13 on 2024-06-15 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_notificationsetting_interval_minutes'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationsetting',
            name='has_alerted',
            field=models.BooleanField(default=False),
        ),
    ]
