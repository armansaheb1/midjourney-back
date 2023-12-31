# Generated by Django 4.2.7 on 2023-11-23 02:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0041_alter_bonus_code_alter_coupon_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonus',
            name='code',
            field=models.CharField(default='zwFMcLzN', max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(default='CM7Epmeg', max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='UsedBonus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bonus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.bonus')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
