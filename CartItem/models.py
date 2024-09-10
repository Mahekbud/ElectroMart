from django.db import models
import uuid
from django.utils import timezone




class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    cart_id = models.ForeignKey('Cart.Cart',  on_delete=models.CASCADE,related_name='cartitems')
    product_id = models.ForeignKey('Product.Product', on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  
    create_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart ID {self.cart.id}"