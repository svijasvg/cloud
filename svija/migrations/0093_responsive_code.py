# Generated by Django 3.0.7 on 2020-07-29 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0092_auto_20200728_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='responsive',
            name='code',
            field=models.CharField(blank=True, default='', max_length=2, verbose_name='two-letter code'),
        ),
    ]
