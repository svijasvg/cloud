# Generated by Django 3.2.7 on 2022-03-01 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0190_rename_to_page_redirect_to_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='font',
            old_name='css',
            new_name='svg_name',
        ),
    ]
