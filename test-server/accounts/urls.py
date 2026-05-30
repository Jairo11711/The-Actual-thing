from django.urls import path
from .import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('registration', views.registration, name='registration'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('view_cart', views.view_cart, name='view_cart'),
    path('remove_cart_item/<int:item_id>', views.remove_item, name='remove_item'),
    path('delivery', views.view_order, name='view_order'),
    path('order_cart', views.order_cart, name='order_cart'),
]
