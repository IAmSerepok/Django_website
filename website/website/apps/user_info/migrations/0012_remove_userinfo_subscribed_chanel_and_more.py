# Generated by Django 4.2.6 on 2023-12-24 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0011_chanel_userinfo_subscribed_chanel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='subscribed_chanel',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='is_subscribed',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Chanel',
        ),
    ]
