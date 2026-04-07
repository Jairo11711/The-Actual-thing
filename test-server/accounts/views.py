from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'accounts/base.html')

def registration(request):
    return render(request, 'accounts/registration_form.html')


def logging(request):
    return render(request, 'accounts/logging_form.html')