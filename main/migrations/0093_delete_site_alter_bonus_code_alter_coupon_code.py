# Generated by Django 4.2.7 on 2024-08-25 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0092_remove_link_have_remove_link_site_remove_link_size_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Site',
        ),
        migrations.AlterField(
            model_name='bonus',
            name='code',
            field=models.CharField(blank=True, default='fPzbPs6k', max_length=8),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(default='OvLelhFv', max_length=8, null=True),
        ),
    ]
