# Generated by Django 4.2.7 on 2023-11-23 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_alter_bonus_code_alter_bonus_user_alter_coupon_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonus',
            name='code',
            field=models.CharField(default='Zw2ixKYP', max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(default='VihpHxXw', max_length=8, null=True),
        ),
    ]
