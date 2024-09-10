from django.urls import path
from .views import create_cart,get_cart_by_id,update_cart_by_id,delete_cart_by_id

urlpatterns = [
    path('create_cart/', create_cart, name='create_cart'),
    path('get_cart_by_id/',get_cart_by_id,name='get_cart_by_id'),
    path('update_cart_by_id/',update_cart_by_id,name='update_cart_by_id'),
    path('delete_cart_by_id/',delete_cart_by_id,name='delete_cart_by_id')
]
