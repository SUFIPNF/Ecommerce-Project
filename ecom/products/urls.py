from django.urls import path
from . import views

urlpatterns = [
    
    path('store/',views.store,name="store"),
    path('store/<category_slug>/',views.store,name='products_by_category'),
    path('product_detail/<category_slug>/<product_slug>/',views.product_detail,name="product_detail")
]