from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import Customer,Item,Transaction,CartItem,Cart


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


# Register your models here.