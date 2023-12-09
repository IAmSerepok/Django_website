# from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render


def index(request):
    return render(request, 'AboutUs/index.html')

def news(request):
    return render(request, 'News/index.html')

def docs(request):
    return render(request, 'Documents/index.html')

def create_account(request):
    return render(request, 'registration/create_account.html')
