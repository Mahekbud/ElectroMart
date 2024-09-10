from django.urls import path
from .views import create_product,get_product_by_id,get_all_products,update_product_by_id,delete_product_by_id,search_product_by_product_name

urlpatterns = [
    
    path('create_product/',create_product,name='create_product'),
    path('get_product_by_id/',get_product_by_id,name='get_product_by_id'),
    path('get_all_products/',get_all_products,name='get_all_products'),
    path('update_product_by_id/',update_product_by_id,name='update_product_by_id'),
    path('delete_product_by_id/',delete_product_by_id,name='delete_product_by_id'),
    path('search_product_by_product_name/',search_product_by_product_name,name='search_product_by_product_name')
    
    
    
]