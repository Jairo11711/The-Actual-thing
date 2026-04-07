from django.contrib import admin
from .models import customer,item,transaction


@admin.register(customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_created', 'id')

    search_fields = ('name',)

    list_filter = ('date_created',)

    readonly_fields = ('date_created',)

    ordering = ('-date_created', )

@admin.register(item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price','date_created', 'id')

    search_fields = ('name',)

    list_filter = ('date_created',)

    readonly_fields = ('date_created',)

    ordering = ('-date_created', )

@admin.register(transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'item', 'date_created', 'id')

    search_fields = ('customer',)

    list_filter = ('date_created',)

    readonly_fields = ('date_created',)

    ordering = ('-date_created', )


# Register your models here.