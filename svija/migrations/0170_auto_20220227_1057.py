# Generated by Django 3.2.7 on 2022-02-27 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0169_remove_responsive_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='optional_script',
        ),
        migrations.DeleteModel(
            name='OptionalScript',
        ),
    ]
