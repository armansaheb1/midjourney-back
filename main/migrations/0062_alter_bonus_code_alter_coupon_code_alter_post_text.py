# Generated by Django 4.2.7 on 2023-12-12 21:41

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0061_alter_bonus_code_alter_coupon_code_alter_post_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonus',
            name='code',
            field=models.CharField(blank=True, default='psonjjXC', max_length=8),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(default='fECH3F1Y', max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]