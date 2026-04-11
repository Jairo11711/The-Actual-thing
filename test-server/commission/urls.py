from django.urls import path
from .import views

app_name = 'commission'

urlpatterns = [
    path('', views.index, name='index'),
]
