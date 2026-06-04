from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import Customer, Item, Transaction, CartItem, Cart, Order, OrderItem


# --- CART INLINES ---

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('item', 'quantity', 'subtotal')  # Completely locked
    max_num = 0                                          # Disables "Add Another" row
    
    def has_delete_permission(self, request, obj=None):
        return False                                     # Removes delete checkbox


class CartInline(admin.StackedInline):
    model = Cart
    extra = 0
    can_delete = False
    show_change_link = True 
    max_num = 0
    
    readonly_fields = ('display_cart_items', 'total_price_display')

    def display_cart_items(self, obj):
        if not obj or not obj.pk:
            return "No cart items to display."

        items = obj.items.all() 
        if not items:
            return "This cart is empty."
        
        html_elements = []
        for item in items:
            subtotal_formatted = f"{item.subtotal:.2f}"
            html_elements.append(
                format_html(
                    "<li><strong>{}x</strong> {} — (₱{})</li>", 
                    item.quantity, 
                    item.item.name, 
                    subtotal_formatted
                )
            )
        
        return format_html("<ul>{}</ul>", mark_safe("".join(html_elements)))
    
    def total_price_display(self, obj):
        if not obj or not obj.pk:
            return "₱0.00"
            
        return f"₱{obj.total_price:.2f}"
    
    display_cart_items.short_description = "Items in Cart"
    total_price_display.short_description = "Current Total"


# --- ORDER INLINES ---

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    # Locked all fields securely to preserve immutable delivery records
    readonly_fields = ('item', 'item_name', 'price_at_purchase', 'quantity', 'subtotal')
    max_num = 0
    
    def has_delete_permission(self, request, obj=None):
        return False


# --- CORE MODELS ADMIN ---

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_created', 'id')
    search_fields = ('name',)
    list_filter = ('date_created',)
    readonly_fields = ('date_created',)
    ordering = ('-date_created', )
    inlines = [CartInline]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    # 1. Added is_in_stock to the main column grid display
    list_display = ('id', 'name', 'price', 'is_in_stock', 'date_created')
    
    # 2. NEW: Allows editing the stock status directly on the list layout view page
    list_editable = ('is_in_stock',)
    
    # 3. Added stock status filter to sidebar queue lists
    list_filter = ('is_in_stock', 'date_created')
    
    search_fields = ('name',)
    readonly_fields = ('date_created',)
    ordering = ('-date_created',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'item', 'date_created', 'id')
    search_fields = ('customer__name',)  # Look up customer by profile name string
    list_filter = ('date_created',)
    readonly_fields = ('date_created',)
    ordering = ('-date_created', )


# --- ORDER MANAGEMENT ADMIN ---
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # 1. Updated display columns to show method, payment status, and delivery status
    list_display = ('id', 'full_name', 'barangay', 'payment_method', 'payment_status', 'delivery_status', 'total_price_display', 'date_ordered')
    
    # 2. Updated filters for quick processing queues (e.g., finding what needs GCash verification)
    list_filter = ('payment_method', 'payment_status', 'delivery_status', 'date_ordered', 'barangay')
    
    search_fields = ('full_name', 'mobile_number', 'street_address', 'gcash_reference', 'gcash_number')
    ordering = ('-date_ordered',)
    
    inlines = [OrderItemInline]
    
    # 3. Reorganized sections to keep Payment/Financial logs completely separate from Delivery Logs
    fieldsets = (
        ('Order Fulfillment', {
            'fields': ('delivery_status', 'total_price_display', 'display_order_items')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'payment_status', 'gcash_number', 'gcash_reference', 'display_payment_proof')
        }),
        ('Customer Contact Profile', {
            'fields': ('customer', 'full_name', 'mobile_number')
        }),
        ('Delivery Location (Urdaneta City)', {
            'fields': ('street_address', 'barangay', 'landmarks', 'address_type', 'postal_code', 'city', 'province', 'region')
        }),
    )
    
    # 4. Kept critical reference nodes readonly while allowing staff to manage statuses
    readonly_fields = (
        'date_ordered', 'total_price_display', 'display_order_items', 'display_payment_proof',
        'postal_code', 'city', 'province', 'region', 
        'customer', 'full_name', 'mobile_number', 'street_address', 'barangay', 'landmarks', 'address_type',
        'payment_method', 'gcash_number', 'gcash_reference'
    )

    def display_order_items(self, obj):
        if not obj or not obj.pk:
            return "No items recorded."
            
        items = obj.order_items.all()
        if not items:
            return "This order has no items."
            
        html_elements = []
        for item in items:
            subtotal_formatted = f"{item.subtotal:.2f}"
            html_elements.append(
                format_html(
                    "<li><strong>{}x</strong> {} — (₱{})</li>",
                    item.quantity,
                    item.item_name,
                    subtotal_formatted
                )
            )
        return format_html("<ul>{}</ul>", mark_safe("".join(html_elements)))

    def total_price_display(self, obj):
        if not obj or not obj.pk:
            return "₱0.00"
        return f"₱{obj.grand_total:.2f}"

    # 5. Helper method to render an image thumbnail preview inside Django admin
    def display_payment_proof(self, obj):
        if obj.payment_proof:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-height: 250px; max-width: 100%; border-radius: 4px; border: 1px solid #ccc;" /></a>',
                obj.payment_proof.url,
                obj.payment_proof.url
            )
        if obj.payment_method == 'gcash':
            return "No payment proof uploaded yet."
        return "Not applicable (COD Order)."

    display_order_items.short_description = "Ordered Items Snapshot"
    total_price_display.short_description = "Grand Total"
    display_payment_proof.short_description = "GCash Receipt Preview"