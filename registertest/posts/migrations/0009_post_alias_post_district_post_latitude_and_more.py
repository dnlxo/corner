# Generated by Django 4.0.2 on 2022-03-02 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_post_like_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='alias',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='district',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='latitude',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='longitude',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='road_address',
            field=models.TextField(blank=True),
        ),
    ]
