# Generated by Django 2.0.13 on 2019-05-04 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0002_auto_20190503_1545'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrokGenerator',
            fields=[
                ('regexgenerator_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='generator.RegexGenerator')),
                ('grok', models.CharField(max_length=10000)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('generator.regexgenerator',),
        ),
    ]
