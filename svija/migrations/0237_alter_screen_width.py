# Generated by Django 3.2.7 on 2022-12-02 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0236_auto_20220926_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screen',
            name='width',
            field=models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Artboard pixel width'),
        ),
    ]
