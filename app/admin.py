from django.contrib import admin
from .models import Product, Review, OrderItem, Order, ShippingAddress, ProductImage
# Register your models here.
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Review)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(ShippingAddress)
