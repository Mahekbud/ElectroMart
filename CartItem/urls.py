from django.urls import path
from .views import create_cartitem,get_cartitem_by_id,update_cartitem_by_id,delete_cartitem_by_id,get_all_cartitems

urlpatterns = [
    path('create_cartitem/', create_cartitem, name='create_cartitem'),
    path('get_cartitem_by_id/',get_cartitem_by_id,name='get_cartitem_by_id'),
    path('update_cartitem_by_id/',update_cartitem_by_id,name='update_cartitem_by_id'),
    path('delete_cartitem_by_id/',delete_cartitem_by_id,name='delete_cartitem_by_id'),
    path('get_all_cartitems/',get_all_cartitems,name='get_all_cartitems')
]
