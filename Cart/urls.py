from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart/add', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),   
]
