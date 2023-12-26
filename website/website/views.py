import os
from django.shortcuts import render
from django.contrib.auth.models import User
from website.apps.user_info.models import (Numeral, StudyingProgram,
                                           UserInfo, Subscribe, Quiz, Language)
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
                            phone_number=form.cleaned_data['phone'])
            info.save()
            numbers = form.cleaned_data['favorite_numbers']
            for num in numbers:
                info.favorite_num.add(Numeral.objects.get(numeral=num))
            return render(request, 'registration/thx.html', {'first': form.cleaned_data['first_name'],
                                                             'second': form.cleaned_data['second_name'],
                                                             'town': form.cleaned_data['town'],
                                                             'phone': form.cleaned_data['phone']})
    else:
        form = CreateUserForm()

    return render(request, 'registration/create_account.html', {'form': form})


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
    name = request.POST.get('name')
    good_program = request.POST.get('my_good_program')
    favorite_png = request.POST.get('favorite_png')

    obj = Quiz(name=name, good_program=good_program,
               favorite_picture=favorite_png)
    obj.save()

    for i in range(5):
        if request.POST.get('favorite' + str(i+1)) == '1':
            obj.language.add(Language.objects.get(id=i+1))

    response_data = {'message': 'Данные успешно обработаны'}
    return JsonResponse(response_data)


def get_statistic(request):
    # Получение данных
    count_of_people = 0
    good_program = [0, 0]
    favorite_picture = [0, 0, 0]
    language = [0, 0, 0, 0, 0]

    for obj in Quiz.objects.values():

        count_of_people += 1

        if obj['good_program'] == 'good':
            good_program[0] += 1
        else:
            good_program[1] += 1

        favorite_picture[int(obj['favorite_picture'])-1] += 1

    for obj in Quiz.objects.all():
        for sub in obj.language.values():
            language[sub['id']-1] += 1

    good_program_res = [int(100*good_program[0]/count_of_people),
                        int(100*good_program[1]/count_of_people)]
    favorite_picture_res = [int(100*favorite_picture[0]/count_of_people),
                            int(100*favorite_picture[1]/count_of_people),
                            int(100*favorite_picture[2]/count_of_people)]
    language_res = [int(100*language[0]/count_of_people),
                    int(100*language[1]/count_of_people),
                    int(100*language[2]/count_of_people),
                    int(100*language[3]/count_of_people),
                    int(100*language[4]/count_of_people)]

    data = {'program': good_program_res,
            'favorite': favorite_picture_res,
            'language': language_res}
    return JsonResponse(data)
