from django.shortcuts import render
from django.shortcuts import redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from dashboard.models import Item, Cart, CartItem, Customer

# Create your views here.
def index(request):
    all_items = Item.objects.all()

    return render(request, 'shop/shop_page.html', {"items" : all_items})

@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Item, id=product_id)
        customer_profile = request.user.customer
        user_cart, created = Cart.objects.get_or_create(customer=customer_profile)
        
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=user_cart, 
            item=product
        )
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
            
        return redirect(request.META.get('HTTP_REFERER', '/'))