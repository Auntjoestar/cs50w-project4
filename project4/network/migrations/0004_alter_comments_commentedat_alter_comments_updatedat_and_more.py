# Generated by Django 5.0.6 on 2024-06-30 03:37

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_alter_comments_commentedat_alter_comments_updatedat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='commentedAt',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 3, 37, 57, 606478, tzinfo=datetime.timezone.utc), verbose_name='Posted at'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='updatedAt',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 3, 37, 57, 606489, tzinfo=datetime.timezone.utc), verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='followers',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 3, 37, 57, 604547, tzinfo=datetime.timezone.utc), verbose_name='Followed at'),
        ),
        migrations.AlterField(
            model_name='pictures',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 3, 37, 57, 607461, tzinfo=datetime.timezone.utc), verbose_name='Uploaded at'),
        ),
        migrations.AlterField(
            model_name='post',
            name='postTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 3, 37, 57, 605395, tzinfo=datetime.timezone.utc), verbose_name='Posted at'),
        ),
        migrations.AlterField(
            model_name='post',
            name='updateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 3, 37, 57, 605405, tzinfo=datetime.timezone.utc), verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 3, 37, 57, 604260, tzinfo=datetime.timezone.utc), verbose_name='Joined at'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 3, 37, 57, 604277, tzinfo=datetime.timezone.utc), verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Username'),
        ),
        migrations.AlterField(
            model_name='profilepictures',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 3, 37, 57, 605104, tzinfo=datetime.timezone.utc), verbose_name='Uploaded AT'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='UpdatedAt',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 3, 37, 57, 607101, tzinfo=datetime.timezone.utc), verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='repliedAt',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 3, 37, 57, 607090, tzinfo=datetime.timezone.utc), verbose_name='Replied at'),
        ),
    ]
