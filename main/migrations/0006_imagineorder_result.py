# Generated by Django 4.2.7 on 2023-11-10 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_imagineorder_done_imagineorder_percent'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagineorder',
            name='result',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
