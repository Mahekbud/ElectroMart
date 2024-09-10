from django.urls import path
from .views import create_shipping,get_shipping_by_id,get_all_shipping,update_shipping_by_id,delete_shipping_by_id,get_shipping_by_status

urlpatterns = [
    path('create_shipping/', create_shipping, name='create_shipping'),
    path('get_shipping_by_id/',get_shipping_by_id,name='get_shipping_by_id'),
    path('get_all_shipping/',get_all_shipping,name='get_all_shipping'),
    path('update_shipping_by_id/',update_shipping_by_id,name='update_shipping_by_id'),
    path('delete_shipping_by_id/',delete_shipping_by_id,name='delete_shipping_by_id'),
    path('get_shipping_by_status/',get_shipping_by_status,name='get_shipping_by_status')
]
