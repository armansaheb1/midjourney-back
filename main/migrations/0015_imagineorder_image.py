# Generated by Django 4.2.7 on 2023-11-13 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagineorder',
            name='image',
            field=models.URLField(null=True),
        ),
    ]
