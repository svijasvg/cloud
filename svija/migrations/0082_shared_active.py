# Generated by Django 3.0.7 on 2020-07-01 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0081_remove_page_shared'),
    ]

    operations = [
        migrations.AddField(
            model_name='shared',
            name='active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
    ]
