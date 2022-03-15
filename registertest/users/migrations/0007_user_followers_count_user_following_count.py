# Generated by Django 4.0.2 on 2022-03-04 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_profile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='following_count',
            field=models.IntegerField(default=0),
        ),
    ]