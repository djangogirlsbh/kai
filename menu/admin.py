from django.contrib import admin
from .models import Item, Order, OrderItem


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'finished_time', 'total_price', 'active')

admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
