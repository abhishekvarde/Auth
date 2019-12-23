# Generated by Django 3.0 on 2019-12-19 08:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0004_auto_20191219_1302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otp',
            name='phone_no',
        ),
        migrations.AddField(
            model_name='otp',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
