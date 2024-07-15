# Generated by Django 5.0.6 on 2024-07-15 23:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_alter_post_posttime_alter_post_updatetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='postTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 15, 23, 41, 40, 34809, tzinfo=datetime.timezone.utc), verbose_name='Posted at'),
        ),
        migrations.AlterField(
            model_name='post',
            name='updateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 15, 23, 41, 40, 34834, tzinfo=datetime.timezone.utc), verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 15, 23, 41, 40, 32575, tzinfo=datetime.timezone.utc), verbose_name='Joined at'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 15, 23, 41, 40, 32650, tzinfo=datetime.timezone.utc), verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='profilepictures',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 15, 23, 41, 40, 34137, tzinfo=datetime.timezone.utc), verbose_name='Uploaded AT'),
        ),
    ]