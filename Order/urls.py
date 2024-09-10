from django.urls import path
from .views import create_order,get_order_by_id,get_all_orders,update_order_by_id,delete_order_by_id,get_orders_by_user,get_order_statistics

urlpatterns = [
    
    path('create_order/',create_order,name='create_order'),
    path('get_order_by_id/',get_order_by_id,name='get_order_by_id'),
    path('get_all_orders/',get_all_orders,name='get_all_orders'),
    path('update_order_by_id/',update_order_by_id,name='update_order_by_id'),
    path('delete_order_by_id/',delete_order_by_id,name='delete_order_by_id'),
    path('get_orders_by_user/',get_orders_by_user,name='get_orders_by_user'),
    path('get_order_statistics/',get_order_statistics,name='get_order_statistics')
    
    
]