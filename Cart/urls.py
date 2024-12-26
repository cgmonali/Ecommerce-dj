from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart/add', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/checkout', views.checkout, name='checkout'),  
    path('cart/clear_store', views.clear_store, name='clear_store'),
]
