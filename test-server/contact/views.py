from django.shortcuts import render

def index(request):
    return render(request, 'contact/base_contact.html')
