# Generated by Django 4.2.7 on 2023-12-12 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0059_post_alter_bonus_code_alter_coupon_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonus',
            name='code',
            field=models.CharField(blank=True, default='p7i8NbLt', max_length=8),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(default='UFm88wuV', max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(),
        ),
    ]
