# Generated by Django 2.0.13 on 2019-05-06 15:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_clientserver_last_run'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientserver',
            name='last_run',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
