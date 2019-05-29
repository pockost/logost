# Generated by Django 2.0.13 on 2019-05-29 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0007_vsftpdgenerator'),
    ]

    operations = [
        migrations.CreateModel(
            name='SshdGenerator',
            fields=[
                ('grokgenerator_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='generator.GrokGenerator')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('generator.grokgenerator',),
        ),
    ]