# Generated by Django 4.2.1 on 2025-06-10 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0328_remove_font_adobe_pasted_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='font',
            options={'ordering': ['-enabled', 'category', 'family', 'weight', 'svg_ref'], 'verbose_name': 'font', 'verbose_name_plural': 'font model list'},
        ),
    ]
