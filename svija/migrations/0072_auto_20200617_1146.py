# Generated by Django 3.0.7 on 2020-06-17 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0071_auto_20200424_1705'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settings',
            name='backup_interval',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='backup_next',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='cache_reset',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='settings',
            name='p3_color',
            field=models.BooleanField(default=False, verbose_name='display P3 color space where possible'),
        ),
    ]
