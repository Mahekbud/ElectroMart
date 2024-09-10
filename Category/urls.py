from django.urls import path
from .views import create_category,get_category_by_id,get_all_categories,update_category_by_id,delete_category_by_id

urlpatterns = [
    
    path('create_category/',create_category,name='create_category'),
    path('get_category_by_id/',get_category_by_id,name='get_category_by_id'),
    path('get_all_categories/',get_all_categories,name='get_all_categories'),
    path('update_category_by_id/',update_category_by_id,name='update_category_by_id'),
    path('delete_category_by_id/',delete_category_by_id,name='delete_category_by_id')
    
    
]