# Generated by Django 3.2.7 on 2021-11-05 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0151_auto_20211105_0933'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='module',
            options={'ordering': ['-published', 'sort1', 'name', 'screen'], 'verbose_name_plural': '2.2 · Modules'},
        ),
        migrations.RenameField(
            model_name='module',
            old_name='active',
            new_name='published',
        ),
    ]
