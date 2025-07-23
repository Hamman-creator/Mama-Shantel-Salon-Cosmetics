from django.contrib import admin
from .models import (
    CustomUser, ProductCategory, Product,
    HairstyleCategory, Hairstyle, Booking, Order
)
from.models import CustomUser,ContactMessage

# Register all models
admin.site.register(CustomUser)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(HairstyleCategory)
admin.site.register(Hairstyle)
admin.site.register(Booking)
admin.site.register(Order)
admin.site.register(ContactMessage)



