# Generated by Django 5.0.6 on 2024-06-30 21:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_alter_comments_commentedat_alter_comments_updatedat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='commentedAt',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 21, 17, 26, 800245, tzinfo=datetime.timezone.utc), verbose_name='Posted at'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='updatedAt',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 21, 17, 26, 800256, tzinfo=datetime.timezone.utc), verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='pictures',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 21, 17, 26, 801176, tzinfo=datetime.timezone.utc), verbose_name='Uploaded at'),
        ),
        migrations.AlterField(
            model_name='post',
            name='postTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 21, 17, 26, 799211, tzinfo=datetime.timezone.utc), verbose_name='Posted at'),
        ),
        migrations.AlterField(
            model_name='post',
            name='updateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 21, 17, 26, 799221, tzinfo=datetime.timezone.utc), verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 21, 17, 26, 798134, tzinfo=datetime.timezone.utc), verbose_name='Joined at'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 21, 17, 26, 798167, tzinfo=datetime.timezone.utc), verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='profilepictures',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 21, 17, 26, 798780, tzinfo=datetime.timezone.utc), verbose_name='Uploaded AT'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='UpdatedAt',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 21, 17, 26, 800882, tzinfo=datetime.timezone.utc), verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='repliedAt',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 21, 17, 26, 800870, tzinfo=datetime.timezone.utc), verbose_name='Replied at'),
        ),
    ]
