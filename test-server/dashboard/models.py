from django.db import models
from django.utils import timezone


class item(models.Model):
    id = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class transaction(models.Model):
    id = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)

    
    customer = models.ForeignKey('customer', on_delete=models.CASCADE)
    item = models.ForeignKey('item', on_delete=models.CASCADE)

    
    def __str__(self):
        return (f"{self.customer.name} bought {self.item.name}")

class customer(models.Model):
    id = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=100)
    # address = models.CharField(max_length=200)
    # email = models.EmailField()
    # phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name