# Generated by Django 4.2.7 on 2023-11-23 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_rename_percent_bonus_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonus',
            name='code',
            field=models.CharField(default='ToE5CqEa', max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(default='N61RxPDG', max_length=8, null=True),
        ),
    ]
