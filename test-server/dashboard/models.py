from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from decimal import Decimal
from django.db.models import Sum, F


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    image = models.ImageField(upload_to="products/", null=True, blank=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)

    
    customer = models.ForeignKey('customer', on_delete=models.CASCADE)
    item = models.ForeignKey('item', on_delete=models.CASCADE)

    
    def __str__(self):
        return (f"{self.customer.name} bought {self.item.name}")

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(default='placeholder@example.com')
    phone_number = models.CharField(max_length=20, default="09876543210")

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE, 
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Added a fallback string in case customer or user isn't assigned yet
        username = self.customer.user.username if self.customer and self.customer.user else "Unknown"
        return f"Cart for {username}"

    @property
    def total_price(self):
        # 2. Let the database multiply quantity * price and sum them up
        result = self.items.aggregate(
            total=Sum(F('quantity') * F('item__price'), output_field=models.DecimalField())
        )['total']
        
        return result if result is not None else Decimal('0.00')
    
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"

    @property
    def subtotal(self):
        return self.item.price * self.quantity