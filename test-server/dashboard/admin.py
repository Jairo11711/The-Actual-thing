from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import Customer,Item,Transaction,CartItem,Cart,Order,OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('subtotal',)

class CartInline(admin.StackedInline):
    model = Cart
    extra = 0
    can_delete = False
    show_change_link = True 
    
    readonly_fields = ('display_cart_items', 'total_price_display')

    def display_cart_items(self, obj):
        # 1. Handle empty/new customer inline form safely
        if not obj or not obj.pk:
            return "No cart items to display."

        items = obj.items.all() 
        # 2. Handle empty cart safely without triggering the format_html error
        if not items:
            return "This cart is empty."
        
        # 3. Use format_html correctly by passing variables as args
        html_elements = []
        for item in items:
            subtotal_formatted = f"{item.subtotal:.2f}"
            # {} placeholders are filled by the trailing arguments safely
            html_elements.append(
                format_html(
                    "<li><strong>{}x</strong> {} — (${})</li>", 
                    item.quantity, 
                    item.item.name, 
                    subtotal_formatted
                )
            )
        
        # Combine them safely inside a <ul> wrapper
        return format_html("<ul>{}</ul>", mark_safe("".join(html_elements)))
    
    def total_price_display(self, obj):
        if not obj or not obj.pk:
            return "$0.00"
            
        return f"${obj.total_price:.2f}"
    
    display_cart_items.short_description = "Items in Cart"
    total_price_display.short_description = "Current Total"

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    # Make order items read-only in the inline view to preserve delivery history integrity
    readonly_fields = ('item_name', 'price_at_purchase', 'quantity', 'subtotal')
    can_delete = False


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
    list_display = ('name', 'price','date_created', 'id')

    search_fields = ('name',)

    list_filter = ('date_created',)

    readonly_fields = ('date_created',)

    ordering = ('-date_created', )

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'item', 'date_created', 'id')

    search_fields = ('customer',)

    list_filter = ('date_created',)

    readonly_fields = ('date_created',)

    ordering = ('-date_created', )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'barangay', 'status', 'total_price_display', 'date_ordered')
    list_filter = ('status', 'date_ordered', 'barangay')
    search_fields = ('full_name', 'mobile_number', 'street_address')
    ordering = ('-date_ordered',)
    
    inlines = [OrderItemInline]
    
    # Organize delivery detail groupings cleanly inside the dashboard panel
    fieldsets = (
        ('Order Status', {
            'fields': ('status', 'total_price_display', 'display_order_items')
        }),
        ('Customer Info', {
            'fields': ('customer', 'full_name', 'mobile_number')
        }),
        ('Delivery Address (Urdaneta City)', {
            'fields': ('street_address', 'barangay', 'landmarks', 'address_type', 'postal_code', 'city', 'province', 'region')
        }),
    )
    
    readonly_fields = ('date_ordered', 'total_price_display', 'display_order_items', 'postal_code', 'city', 'province', 'region')

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

    display_order_items.short_description = "Ordered Items Snapshot"
    total_price_display.short_description = "Grand Total Amount"