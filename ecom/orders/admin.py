from django.contrib import admin
from .models import Orders,OrderProduct,Payment
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display=['user','order_number','first_name','last_name','phone','order_total','status']
class OrderProductAdmin(admin.ModelAdmin):
    list_display=['order','product','user','quantity','price']

class PaymentAdmin(admin.ModelAdmin):
    list_display=['user','payment_id','payment_method','amount_paid']
admin.site.register(Orders,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)
admin.site.register(Payment,PaymentAdmin)