# Generated by Django 4.2.7 on 2023-11-04 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_link_size_alter_link_sizes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='sizes',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
        migrations.AddField(
            model_name='link',
            name='sizes',
            field=models.JSONField(blank=True, editable=False, null=True),
        ),
    ]
