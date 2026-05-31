from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomerRegistrationForm, CustomerProfileForm
from dashboard.models import Cart, CartItem, Order,OrderItem
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'accounts/base_accounts.html')

def registration(request):
    if request.method == "POST" and request.POST.get("action") == "REGISTER":
        user_form = CustomerRegistrationForm(request.POST)
        profile_form = CustomerProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, f"Success: Account created for {user.username}! ")
            return redirect('accounts:login')
    else:
        user_form = CustomerRegistrationForm()
        profile_form = CustomerProfileForm()
        


    return render(request, 'accounts/registration_form.html', {
        'user_form': user_form, 
        'profile_form': profile_form
    })


def login_user(request):
    if request.method == "POST" and request.POST.get("action") == "LOGIN":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:index')
        else:
            messages.error(request, "Error: Please Try Again")
            return redirect('accounts:login')
        
    else: 
        return render(request, 'accounts/login_form.html', {})

def logout_user(request):
    logout(request)
    return redirect('main:index')

@login_required
def view_cart(request):
    try:
        # 1. Get the cart belonging to the logged-in user's customer profile
        # select_related and prefetch_related optimize the database query to fetch items/images fast
        cart = Cart.objects.select_related('customer').prefetch_related('items__item').get(customer__user=request.user)
    except Cart.DoesNotExist:
        # If the user doesn't have a cart yet, we pass None
        cart = None
    
    context = {
        'cart': cart
    }
    return render(request, 'accounts/checkout.html', context)

def remove_item(request, item_id):
    if request.method == 'POST' and request.user.is_authenticated:
        # Secure the query by chaining it down from the logged-in user
        cart_item = get_object_or_404(
            CartItem, 
            id=item_id, 
            cart__customer__user=request.user
        )
        cart_item.delete()
        messages.success(request, "Item removed from your cart.")
        
    return redirect(request.META.get('HTTP_REFERER', 'accounts:view_cart'))



@login_required
def order_cart(request):
    # 1. FIXED RELATION LOOKUP: Find cart through the customer attribute, just like view_cart does
    cart = get_object_or_404(Cart, customer__user=request.user)
    cart_items = cart.items.all()
    print("called out")
    if not cart_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('accounts:view_cart')

    if request.method == 'POST' and request.POST.get("action") == "ORDER":
        
        print("called in")
        # 2. Extract clean form parameters
        full_name = request.POST.get('full_name')
        mobile_number = request.POST.get('mobile_number')
        street_address = request.POST.get('street_address')
        barangay = request.POST.get('barangay')
        address_type = request.POST.get('address_type', 'home')
        landmarks = request.POST.get('landmarks', '')
        print("step 2")
        # 3. FIXED ORDER INITIALIZATION: Links via customer object instead of auth.User
        order = Order.objects.create(
            customer=cart.customer,
            full_name=full_name,
            mobile_number=mobile_number,
            street_address=street_address,
            barangay=barangay,
            address_type=address_type,
            landmarks=landmarks
        )
        print("step 3")
        # 4. FIXED ATTRIBUTE ACCESSORS: Matches your precise model field naming strategies
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                item=cart_item.item,
                item_name=cart_item.item.name,
                price_at_purchase=cart_item.item.price,
                quantity=cart_item.quantity
            )
        print("step 4")
        # 5. Safe removal of checkout data structures
        cart_items.delete() 
        print("step 5")
        # 6. Redirect onward to delivery dashboard view using the generated transaction primary key
        return redirect('accounts:view_order')

    return redirect('accounts:view_cart')

@login_required
def view_order(request):
    # Fetch all orders for the user, latest first
    customer_orders = Order.objects.filter(customer__user=request.user).order_by('-date_ordered')
    
    # Check if the user clicked a specific order button (e.g., /accounts/delivery/?order=3)
    selected_order_id = request.GET.get('order')
    selected_order = None
    
    if customer_orders.exists():
        if selected_order_id:
            selected_order = customer_orders.filter(id=selected_order_id).first()
        
        # Fallback: If no order ID was clicked (or it was invalid), default to the latest order
        if not selected_order:
            selected_order = customer_orders.first()
            
    context = {
        'orders': customer_orders,
        'selected_order': selected_order  # Pass the single chosen order to the template
    }
    return render(request, 'accounts/delivery.html', context)

def order_detail(request, order_id):
    return render(request, 'accounts/base_accounts.html')

"""
@login_required
def view_order(request, order_id):
    # Fetch specified order safely, confirming validation rules against active user instance
    order = get_object_or_404(Order, id=order_id, customer__user=request.user)
    
    context = {
        'order': order,
        'order_items': order.order_items.all()
    }
    return render(request, 'accounts/delivery.html', context)
"""