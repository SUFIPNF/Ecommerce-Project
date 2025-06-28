from django.contrib import admin
from cart.models import Cart,CartItem
# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display=['cart_id','date_added']
class CartItemAdmin(admin.ModelAdmin):
    list_display=['cart','cart_item','quantity']
admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)