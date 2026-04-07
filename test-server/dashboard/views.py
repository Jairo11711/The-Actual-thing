from django.shortcuts import render
from django.http import HttpResponseRedirect



from .forms import CustomerForm, TransactionForm, ItemForm

# Create your views here.

def index(request):
    return render(request, 'dashboard/dashboard.html')

def db_control(request):
    submitted = False
    
    customer_form = CustomerForm(prefix="customer")
    transaction_form = TransactionForm(prefix="transaction")
    item_form = ItemForm(prefix="item")

    if request.method == "POST":
        if "customer_form" in request.POST:
            customer_form = CustomerForm(request.POST, prefix="customer")
            if customer_form.is_valid():
                customer_form.save()
                return HttpResponseRedirect('/dashboard/db_control?submitted=True')
        
        elif "item_form" in request.POST:
            item_form = ItemForm(request.POST, prefix="item")
            if item_form.is_valid():
                item_form.save()
                return HttpResponseRedirect('/dashboard/db_control?submitted=True')
      
        elif "transaction_form" in request.POST:
            transaction_form = TransactionForm(request.POST, prefix="transaction")
            if transaction_form.is_valid():
                transaction_form.save()
                return HttpResponseRedirect('/dashboard/db_control?submitted=True')
      
    else:
        customer_form = CustomerForm()
        transaction_form = TransactionForm()
        item_form = ItemForm()
        if 'submitted' in request.GET:
            submitted = True
    
    return render(request, "dashboard/db_control.html", {
        "customer_form": customer_form,
        "transaction_form" : transaction_form,
        "item_form" : item_form,
        'submitted': submitted})
