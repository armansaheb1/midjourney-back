# Generated by Django 4.2.7 on 2023-12-12 22:23

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0063_alter_bonus_code_alter_coupon_code_alter_post_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='text',
        ),
        migrations.AddField(
            model_name='post',
            name='content',
            field=ckeditor.fields.RichTextField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bonus',
            name='code',
            field=models.CharField(blank=True, default='VY7Hb4um', max_length=8),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(default='nUJDJCz9', max_length=8, null=True),
        ),
    ]
