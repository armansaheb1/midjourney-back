# Generated by Django 4.2.7 on 2023-12-28 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiService', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
