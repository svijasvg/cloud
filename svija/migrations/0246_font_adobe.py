# Generated by Django 4.1.4 on 2022-12-15 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0245_remove_font_adobe'),
    ]

    operations = [
        migrations.AddField(
            model_name='font',
            name='adobe',
            field=models.TextField(blank=True, default='', max_length=5000, verbose_name='Adobe CSS'),
        ),
    ]
