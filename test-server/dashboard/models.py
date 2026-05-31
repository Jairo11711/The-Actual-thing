from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from decimal import Decimal, ROUND_HALF_UP
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
        # Sums the working subtotal of all items in this cart.
        # Decimal('0.00') provides a safe starting point for Python's sum function.
        return sum((item.subtotal for item in self.items.all()), Decimal('0.00'))

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
        raw_subtotal = self.item.price * self.quantity
        # Kept consistent with the Cart total rounding
        return raw_subtotal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending / Preparing'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    # Form Delivery Details
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=20)
    street_address = models.CharField(max_length=255)
    barangay = models.CharField(max_length=100)
    
    # Locked delivery parameters for your specific business setup
    region = models.CharField(max_length=100, default="Region I (Ilocos Region)")
    province = models.CharField(max_length=100, default="Pangasinan")
    city = models.CharField(max_length=100, default="Urdaneta City")
    postal_code = models.CharField(max_length=10, default="2428")
    
    address_type = models.CharField(max_length=10, choices=[('home', 'Home'), ('office', 'Office')], default='home')
    landmarks = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name} ({self.status})"

    @property
    def grand_total(self):
        # Sums the working subtotal of all items recorded under this historical order.
        return sum((item.subtotal for item in self.order_items.all()), Decimal('0.00'))

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    # Link to item fallback, but save names/prices as strings/decimals 
    # to protect historical orders if a store item gets updated or deleted later.
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    item_name = models.CharField(max_length=100)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item_name} (Order #{self.order.id})"

    @property
    def subtotal(self):
        # FIX: Fallback to 0 if price_at_purchase is missing/None
        price = self.price_at_purchase if self.price_at_purchase is not None else Decimal('0.00')
        
        raw_subtotal = price * self.quantity
        return raw_subtotal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)