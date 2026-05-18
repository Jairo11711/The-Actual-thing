from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomerRegistrationForm, CustomerProfileForm



# Create your views here.
def index(request):
    return render(request, 'accounts/base_accounts.html')

def registration(request):
    if request.method == "POST":
        user_form = CustomerRegistrationForm(request.POST)
        profile_form = CustomerProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, f"Success: Account created for {user.username}! ")
            return redirect('accounts:login')
    else:
        user_form = CustomerRegistrationForm()
        profile_form = CustomerProfileForm()
        


    return render(request, 'accounts/registration_form.html', {
        'user_form': user_form, 
        'profile_form': profile_form
    })


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:index')
        else:
            print("I get hERE")
            messages.error(request, "Error: Please Try Again")
            return redirect('accounts:login')
        
    else: 
        return render(request, 'accounts/login_form.html', {})

def logout_user(request):
    logout(request)
    return redirect('main:index')