# Generated by Django 4.2.7 on 2023-11-18 19:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_remove_faceswaped_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='faceswaped',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
