# Generated by Django 3.2.7 on 2022-03-01 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0200_auto_20220301_1441'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='module',
            options={'ordering': ['-active', 'category', 'order', 'name', 'screen'], 'verbose_name_plural': '2.1 · Modules'},
        ),
        migrations.RenameField(
            model_name='module',
            old_name='horz_offset',
            new_name='offsetx',
        ),
        migrations.RenameField(
            model_name='module',
            old_name='vert_offset',
            new_name='offsety',
        ),
        migrations.RenameField(
            model_name='module',
            old_name='display_order',
            new_name='order',
        ),
    ]
