# Generated by Django 3.2.7 on 2022-03-01 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0203_rename_override_dims_page_override'),
    ]

    operations = [
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limit', models.PositiveIntegerField(default=300, verbose_name='sync folder MB max')),
                ('password', models.CharField(default='', max_length=20, verbose_name='password')),
                ('cached', models.BooleanField(default=False, verbose_name='caching active')),
            ],
            options={
                'verbose_name': 'control',
                'verbose_name_plural': 'Control',
            },
        ),
    ]
