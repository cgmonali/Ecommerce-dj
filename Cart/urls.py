from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout, name='checkout'),  
    path('clear_store/', views.clear_store, name='clear_store'),
    path('get_data/', views.get_data, name='get_data'),
]
