# Generated by Django 2.2.3 on 2019-12-07 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0036_language_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='flag',
            field=models.CharField(blank=True, default='', max_length=2, verbose_name='flag emoji'),
        ),
    ]
