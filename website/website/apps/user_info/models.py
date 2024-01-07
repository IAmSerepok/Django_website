from django.db import models
from django.contrib.auth.models import User


class StudyingProgram(models.Model):
    name = models.CharField(max_length=50)


class Numeral(models.Model):
    numeral = models.CharField(max_length=1)


class UserInfo(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    program = models.ForeignKey(StudyingProgram, null=True, on_delete=models.DO_NOTHING)
    favorite_num = models.ManyToManyField(Numeral)
    town = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)
    third_name = models.CharField(max_length=50, null=True)


class Subscribe(models.Model):
    mail = models.CharField(max_length=20)


class Question(models.Model):
    name = models.CharField(max_length=10)


class Quiz(models.Model):
    school = models.CharField(max_length=50, null=True)
    type = models.CharField(max_length=20, null=True)
    form = models.CharField(max_length=20, null=True)
    answer = models.ManyToManyField(Question)
