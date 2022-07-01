from django.contrib import admin
from Orders.models import Order, OrderItem

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('turniej', 'zawodnik', 'is_paid')
	search_fields = ('turniej', 'zawodnik')

# admin.site.register(Account, WynikiAdmin)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ('order','wynik','is_paid', 'to_pay')
	search_fields = ('order','wynik')

