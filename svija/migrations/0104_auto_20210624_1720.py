# Generated by Django 3.0.7 on 2021-06-24 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0103_auto_20210623_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='prefix',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='svija.Prefix', verbose_name='combination code default'),
        ),
    ]
