# Generated by Django 4.2.1 on 2023-12-19 16:14

from django.db import migrations
import svija.models


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0282_alter_pagescript_script'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screen',
            name='code',
            field=svija.models.alphaAll(default='', max_length=20, verbose_name='artboard name'),
        ),
    ]
