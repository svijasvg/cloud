# Generated by Django 4.2.1 on 2023-06-30 15:40

from django.db import migrations
import svija.models


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0266_alter_module_filename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='illustrator',
            name='filename',
            field=svija.models.addAiToEnd(default='', max_length=200),
        ),
    ]
