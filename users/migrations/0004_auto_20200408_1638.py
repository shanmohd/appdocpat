# Generated by Django 3.0.3 on 2020-04-08 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200407_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='add_appointments',
            name='address',
            field=models.CharField(max_length=200),
        ),
    ]
