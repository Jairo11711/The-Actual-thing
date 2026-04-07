from django.forms import ModelForm
from .models import customer, transaction, item

class CustomerForm(ModelForm):
    class Meta:
        model = customer
        fields = ('name',)
        labels = {
            'name' : 'Customer Name', #This is where you put the label for the fields
        }

class TransactionForm(ModelForm):
    class Meta:
        model = transaction
        fields = ('customer', 'item', )
        labels = {
            'customer' : 'Customer Name',
            'item' : 'Item Name',
        }

class ItemForm(ModelForm):
    class Meta:
        model = item
        fields = {'name', 'price'}
        labels = {
            'name' : 'Item Name',
            'price' : 'Item Price',
        }