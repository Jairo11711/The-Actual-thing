from django.forms import ModelForm
from .models import Customer, Transaction, Item

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ('name',)
        labels = {
            'name' : 'Customer Name', #This is where you put the label for the fields
        }

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('customer', 'item', )
        labels = {
            'customer' : 'Customer Name',
            'item' : 'Item Name',
        }

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = {'name', 'price'}
        labels = {
            'name' : 'Item Name',
            'price' : 'Item Price',
        }