# Generated by Django 4.2.1 on 2025-04-10 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0312_alter_additionalscript_options_alter_robots_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='font',
            name='category',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='tag'),
        ),
        migrations.AlterField(
            model_name='module',
            name='tag',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='tag'),
        ),
        migrations.AlterField(
            model_name='page',
            name='category',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='tag'),
        ),
        migrations.AlterField(
            model_name='script',
            name='category',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='tag'),
        ),
    ]
