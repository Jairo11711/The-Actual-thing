from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, 'accounts/base.html')

def registration(request):
    return render(request, 'accounts/registration_form.html')


def login_user(request):
    return render(request, 'accounts/login_form.html')

def logout_user(request):
    return