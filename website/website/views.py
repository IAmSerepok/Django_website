import os
from django.shortcuts import render
from django.contrib.auth.models import User
from website.apps.user_info.models import (Numeral, StudyingProgram,
                                           UserInfo, Subscribe, Quiz, Question)
from website.apps.user_info.forms import CreateUserForm
from django.contrib.auth import login
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.views import View
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'AboutUs/index.html')


def news(request):
    return render(request, 'News/index.html')


@login_required
def quiz(request):
    return render(request, 'DZ/quiz.html')


def subscribe(request):
    return render(request, 'DZ/subscribe.html')


def create_account(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['user_name'],
                                            password=form.cleaned_data['password'],
                                            first_name=form.cleaned_data['first_name'],
                                            last_name=form.cleaned_data['second_name'])
            login(request, user)
            program = StudyingProgram.objects.get(name=form.cleaned_data['program_name'])
            info = UserInfo(user_id=user.id, program_id=program.id,
                            town=form.cleaned_data['town'],
                            phone_number=form.cleaned_data['phone'],
                            third_name=form.cleaned_data['third_name'])
            info.save()
            numbers = form.cleaned_data['favorite_numbers']
            for num in numbers:
                info.favorite_num.add(Numeral.objects.get(numeral=num))
            return render(request, 'registration/thx.html', {'first': form.cleaned_data['first_name'],
                                                             'second': form.cleaned_data['second_name'],
                                                             'third': form.cleaned_data['third_name'],
                                                             'town': form.cleaned_data['town'],
                                                             'phone': form.cleaned_data['phone']})
        else:
            return render(request, 'registration/create_account.html', {'form': form, 'first': 0})
    else:
        form = CreateUserForm()

        return render(request, 'registration/create_account.html', {'form': form, "first": 1})


@require_POST
@csrf_exempt
def save(request):
    text = request.POST.get('text')

    obj = Subscribe(mail=text)
    obj.save()

    response_data = {'message': 'Данные успешно обработаны'}
    return JsonResponse(response_data)


@require_POST
@csrf_exempt
def save_quiz(request):

    obj = Quiz(school=request.POST.get('program'),
               type=request.POST.get('type'),
               form=request.POST.get('form'))
    obj.save()

    if request.POST.get('answ') != '':
        for my_id in request.POST.get('answ').split(','):
            obj.answer.add(Question.objects.get(id=int(my_id)))

    response_data = {'message': 'Данные успешно обработаны'}
    return JsonResponse(response_data)


def get_statistic(request):
    data = {}

    count_of_people = 0
    who = [
        [0, 0, 0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    answers = [0, 0, 0, 0, 0, 0, 0]

    sub = {
        "ИМКТ": 0, "ПИ": 1, "Восток": 2, "ЮШ": 3, "ШЭМ": 4, "Мед": 5,
        "Бакалавриат": 0, "Магистратура": 1, "Аспирантура": 2,
        "очно": 0, "заочно": 1, "очно-заочно": 2
    }

    for obj in Quiz.objects.values():

        count_of_people += 1

        who[0][sub[obj['school']]] += 1
        who[1][sub[obj['type']]] += 1
        who[2][sub[obj['form']]] += 1

    for obj in Quiz.objects.all():
        for sub in obj.answer.values():
            answers[sub['id']-1] += 1

    ind = 0
    for i in range(5):
        if who[0][i] > who[0][ind]:
            ind = i

    tmp = {0: "ИМКТ", 1: "ПИ", 2: "Института востоковеденья",
           3: "ЮШ", 4: "ШЭМ", 5: "Меда"}

    data['school'] = tmp[ind]

    ind = 0
    for i in range(3):
        if who[1][i] > who[1][ind]:
            ind = i

    tmp = {0: "бaкалавриате", 1: "магистратуре", 2: "аспирантуре"}

    data['type'] = tmp[ind]

    ind = 0
    for i in range(3):
        if who[2][i] > who[2][ind]:
            ind = i

    tmp = {0: "очной", 1: "заочной", 2: "очно-заочной"}

    data['form'] = tmp[ind]

    data['percent'] = [
        int(round(answers[0] / count_of_people*100)),
        int(round(answers[1] / count_of_people*100)),
        int(round(answers[2] / count_of_people*100)),
        int(round(answers[3] / count_of_people*100)),
        int(round(answers[4] / count_of_people*100)),
        int(round(answers[5] / count_of_people*100)),
        int(round(answers[6] / count_of_people*100))
    ]

    return JsonResponse(data)
