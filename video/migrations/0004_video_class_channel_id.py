# Generated by Django 2.2.7 on 2019-12-26 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0003_auto_20191226_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='video_class',
            name='channel_id',
            field=models.IntegerField(default=0),
        ),
    ]
