# Generated by Django 4.2.6 on 2023-12-24 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0016_alter_numeral_numeral'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('good_program', models.CharField(max_length=20, null=True)),
                ('favorite_picture', models.IntegerField()),
                ('language', models.ManyToManyField(to='user_info.language')),
            ],
        ),
    ]