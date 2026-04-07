from django.urls import path
from .import views
from .models import customer,transaction,item

urlpatterns = [
    path('', views.index, name='index'),
    path('db_control', views.db_control, name='db_control')
]