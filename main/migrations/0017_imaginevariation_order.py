# Generated by Django 4.2.7 on 2023-11-13 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_imaginevariation'),
    ]

    operations = [
        migrations.AddField(
            model_name='imaginevariation',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='main.imagineorder'),
        ),
    ]
