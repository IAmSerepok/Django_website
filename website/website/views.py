from django.shortcuts import render
from django.contrib.auth.models import User
from website.apps.user_info.models import UserInfo, Numeral, StudyingProgram
from website.apps.user_info.forms import CreateUserForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.views import View


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
