# Generated by Django 4.2.7 on 2023-11-19 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_plans'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Plans',
            new_name='Plan',
        ),
    ]