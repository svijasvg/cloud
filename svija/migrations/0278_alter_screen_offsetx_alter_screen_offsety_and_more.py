# Generated by Django 4.2.1 on 2023-07-24 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0277_rename_category_module_tag_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screen',
            name='offsetx',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='x offset'),
        ),
        migrations.AlterField(
            model_name='screen',
            name='offsety',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='y offset'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='p3_color',
            field=models.BooleanField(default=True, verbose_name='use "Display P3" color space'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='url',
            field=models.CharField(default='', max_length=200, verbose_name='address'),
        ),
    ]
