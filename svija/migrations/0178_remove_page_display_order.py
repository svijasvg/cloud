# Generated by Django 3.2.7 on 2022-02-27 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0177_remove_settings_secure'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='display_order',
        ),
    ]
