# Generated by Django 3.0.7 on 2021-07-29 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svija', '0114_auto_20210726_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultscripttypes',
            name='type',
            field=models.CharField(choices=[('CSS', 'CSS'), ('head JS', 'head JS'), ('body JS', 'body JS'), ('HTML', 'HTML'), ('form', 'form')], default='', max_length=255, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='language',
            name='form_alert_fail',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='sending failed'),
        ),
        migrations.AlterField(
            model_name='modulescripts',
            name='type',
            field=models.CharField(choices=[('CSS', 'CSS'), ('head JS', 'head JS'), ('body JS', 'body JS'), ('HTML', 'HTML'), ('form', 'form')], default='', max_length=255, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='optionalscript',
            name='type',
            field=models.CharField(choices=[('CSS', 'CSS'), ('head JS', 'head JS'), ('body JS', 'body JS'), ('HTML', 'HTML'), ('form', 'form')], default='', max_length=255, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='pagescripts',
            name='type',
            field=models.CharField(choices=[('CSS', 'CSS'), ('head JS', 'head JS'), ('body JS', 'body JS'), ('HTML', 'HTML'), ('form', 'form')], default='', max_length=255, verbose_name='type'),
        ),
    ]
