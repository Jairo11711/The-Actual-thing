from django.contrib import admin
from dashboard.models import Review

# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # 1. Columns displayed in the admin dashboard list view
    list_display = ('id', 'customer', 'get_order_id', 'get_short_content', 'date_created')
    
    # 2. Filters on the right sidebar to narrow down reviews by time or order status
    list_filter = ('date_created', 'order__delivery_status')
    
    # 3. Search bar functionality (lookup via customer name, username, or text keywords)
    search_fields = ('customer__name', 'customer__user__username', 'content', 'order__id')
    
    # 4. Keeps the auto-generated timestamp read-only
    readonly_fields = ('date_created',)
    
    # 5. Orders the list to show the newest feedback at the top
    ordering = ('-date_created',)

    # Custom helper to display the Order ID clearly in the grid row
    def get_order_id(self, obj):
        if obj.order:
            return f"Order #{obj.order.id}"
        return "N/A"
    get_order_id.short_description = 'Linked Order'

    # Custom helper to clip long paragraphs so they don't break your layout table UI
    def get_short_content(self, obj):
        return obj.content[:60] + "..." if len(obj.content) > 60 else obj.content
    get_short_content.short_description = 'Review Text'