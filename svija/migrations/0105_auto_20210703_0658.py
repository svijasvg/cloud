# Generated by Django 3.0.7 on 2021-07-03 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0104_auto_20210624_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='font',
            name='css',
            field=models.CharField(default='', max_length=100, verbose_name='SVG name'),
        ),
    ]
