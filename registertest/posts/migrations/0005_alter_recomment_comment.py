# Generated by Django 4.0.2 on 2022-02-27 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_comment_contents_recomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recomment',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recomment', to='posts.comment'),
        ),
    ]
