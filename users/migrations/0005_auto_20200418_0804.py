# Generated by Django 3.0.3 on 2020-04-18 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200408_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='add_appointments',
            name='appointment_time_from',
        ),
        migrations.RemoveField(
            model_name='add_appointments',
            name='appointment_time_to',
        ),
    ]
