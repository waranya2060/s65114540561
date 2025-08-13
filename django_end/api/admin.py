from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(BankTransfer)
# admin.site.register(User)
# admin.site.register(Customer)
admin.site.register(Mechanic_Type)
admin.site.register(Mechanic)
admin.site.register(Store)
# admin.site.register(Admin)
admin.site.register(Users)
admin.site.register(Product_Type)
# admin.site.register(Product_Status)
# admin.site.register(Product)
admin.site.register(Money_Status)
admin.site.register(Delivery_Options)
# admin.site.register(Payment_Options)
# admin.site.register(Order)
# admin.site.register(Payment)
# admin.site.register(Order_Product)
# admin.site.register(Carts)
# admin.site.register(Conversations)
# admin.site.register(Sale)
# admin.site.register(Conversations)
# admin.site.register(Storck)
class ProductAdmin(admin.ModelAdmin):
    list_display =['id', 'name', 'price']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id',  'user', ]


# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ['id', 'price', 'quantity', 'product']





admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
# admin.site.register(CartItem, OrderItemAdmin)
# admin.site.register(LineItem, LineItemAdmin)

admin.site.register(OrderItem)
admin.site.register(Payment)