# Generated by Django 4.2.6 on 2023-12-27 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0017_language_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='third_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]