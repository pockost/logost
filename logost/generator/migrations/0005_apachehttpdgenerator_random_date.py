# Generated by Django 2.0.13 on 2019-05-07 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0004_apachehttpdgenerator'),
    ]

    operations = [
        migrations.AddField(
            model_name='apachehttpdgenerator',
            name='random_date',
            field=models.BooleanField(default=True),
        ),
    ]
