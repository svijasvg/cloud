# Generated by Django 3.2.7 on 2021-11-29 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0155_auto_20211129_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='script',
            name='load_order',
            field=models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='load order'),
        ),
    ]
