# Generated by Django 3.0.7 on 2021-07-26 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0109_auto_20210726_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultscripts',
            name='responsive',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='svija.Responsive', verbose_name='screen size'),
        ),
    ]
