from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



# Create your views here.
def index(request):
    return render(request, 'accounts/base_accounts.html')

def registration(request):
    return render(request, 'accounts/registration_form.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Succesfully Logged In")
            return redirect('main:index')
        else:
            messages.success(request, "Error: Please Try Again")
            return redirect('accounts:login')
        
    else: 
        return render(request, 'accounts/login_form.html', {})

def logout_user(request):
    logout(request)
    return redirect('main:index')