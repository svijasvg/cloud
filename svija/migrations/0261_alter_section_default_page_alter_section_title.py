# Generated by Django 4.2.1 on 2023-06-29 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0260_alter_section_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='default_page',
            field=models.CharField(default='', max_length=200, verbose_name='default page address'),
        ),
        migrations.AlterField(
            model_name='section',
            name='title',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='second part of page title'),
        ),
    ]
