# Generated by Django 3.2.7 on 2021-10-28 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0149_auto_20211028_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='instructions',
            field=models.TextField(blank=True, default='', max_length=2000, verbose_name='notes'),
        ),
        migrations.AddField(
            model_name='module',
            name='url',
            field=models.CharField(default='', max_length=60, verbose_name='link'),
        ),
    ]
