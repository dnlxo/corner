# Generated by Django 4.0.2 on 2022-02-22 21:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(upload_to='')),
                ('posts', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='image_post', to='posts.post')),
            ],
        ),
    ]
