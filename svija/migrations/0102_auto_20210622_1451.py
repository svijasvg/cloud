# Generated by Django 3.0.7 on 2021-06-22 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0101_auto_20210618_1417'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='prefix',
            options={'ordering': ['display_order'], 'verbose_name': 'Combination Code', 'verbose_name_plural': '1.4 · Combination Codes'},
        ),
        migrations.AlterField(
            model_name='page',
            name='prefix',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='svija.Prefix', verbose_name='combination code'),
        ),
        migrations.AlterField(
            model_name='page',
            name='url',
            field=models.CharField(default='', max_length=200, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='prefix',
            name='path',
            field=models.CharField(default='', max_length=2, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='prefix',
            name='responsive',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='svija.Responsive', verbose_name='screen'),
        ),
    ]
