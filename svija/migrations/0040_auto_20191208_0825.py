# Generated by Django 2.2.3 on 2019-12-08 07:25

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0039_auto_20191208_0820'),
    ]

    operations = [
        migrations.CreateModel(
            name='Help',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
                ('cat1', models.CharField(blank=True, default='', max_length=100, verbose_name='main category')),
                ('cat2', models.CharField(blank=True, default='', max_length=100, verbose_name='main category')),
                ('link', models.CharField(blank=True, default='', max_length=100, verbose_name='sub category')),
                ('contents', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'help',
                'verbose_name_plural': 'help',
            },
        ),
        migrations.AlterField(
            model_name='notes',
            name='author',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='category',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='category'),
        ),
    ]
