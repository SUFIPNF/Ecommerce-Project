from django.contrib import admin
from .models import Product,Variation
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'product_slug':('name',)}
    list_display=['name','price','stock','image','category']

class VariationAdmin(admin.ModelAdmin):
    list_display=['product','variation_category','variation_value']
admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)