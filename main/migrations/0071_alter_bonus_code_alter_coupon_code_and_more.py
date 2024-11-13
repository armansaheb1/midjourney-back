# Generated by Django 4.2.7 on 2023-12-17 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0070_alter_bonus_code_alter_coupon_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonus',
            name='code',
            field=models.CharField(blank=True, default='hTduILcL', max_length=8),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(default='T4OpgbKb', max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='text',
            field=models.FileField(null=True, upload_to='train'),
        ),
    ]