# Generated by Django 2.0.13 on 2019-05-07 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0006_auto_20190507_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='VsftpdGenerator',
            fields=[
                ('grokgenerator_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='generator.GrokGenerator')),
                ('custom_url', models.CharField(blank=True, default='', max_length=400)),
                ('custom_username', models.CharField(blank=True, default='', max_length=400)),
                ('random_date', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('generator.grokgenerator',),
        ),
    ]
