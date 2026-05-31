from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Commission

@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'email', 'created_at')
    search_fields = ('product_name', 'email', 'details')
    list_filter = ('created_at',)
    ordering = ('-created_at',)