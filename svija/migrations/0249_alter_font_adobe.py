# Generated by Django 4.1.4 on 2023-03-05 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0248_alter_font_adobe_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='font',
            name='adobe',
            field=models.TextField(blank=True, default='', max_length=20000, verbose_name='Adobe CSS'),
        ),
    ]
