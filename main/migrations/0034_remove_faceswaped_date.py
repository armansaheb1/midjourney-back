# Generated by Django 4.2.7 on 2023-11-18 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_faceswaped_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faceswaped',
            name='date',
        ),
    ]
