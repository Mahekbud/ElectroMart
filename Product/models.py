from django.db import models
from django.utils import timezone
import uuid

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)  
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    discount_price = models.IntegerField(blank=True, null=True) 
    category_id = models.ForeignKey('Category.Category', on_delete=models.CASCADE,related_name='product')
    quantity = models.PositiveIntegerField() 
    create_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
  
    
    
    def __str__(self):
        return self.name
