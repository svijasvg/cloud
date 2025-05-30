# Generated by Django 2.2.3 on 2020-04-21 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0061_auto_20200421_1414'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={'ordering': ['display_order', '-pub_date']},
        ),
        migrations.AddField(
            model_name='page',
            name='display_order',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='display order'),
        ),
    ]
