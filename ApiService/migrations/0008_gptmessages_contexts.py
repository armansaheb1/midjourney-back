# Generated by Django 4.2.7 on 2024-03-02 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiService', '0007_alter_gptmessages_context'),
    ]

    operations = [
        migrations.AddField(
            model_name='gptmessages',
            name='contexts',
            field=models.JSONField(null=True),
        ),
    ]