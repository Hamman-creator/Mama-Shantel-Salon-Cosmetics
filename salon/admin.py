from django.contrib import admin
from .models import (
    CustomUser, ProductCategory, Product,
    HairstyleCategory, Hairstyle, Booking, Order,Blog,BlogImage,BlogCategory
)
from.models import CustomUser,ContactMessage



class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 5  

class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogImageInline]
    list_display = ('title', 'category','created_at')
    list_filter= ('category', 'created_at')

# Register all models
admin.site.register(CustomUser)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(HairstyleCategory)
admin.site.register(Hairstyle)
admin.site.register(Booking)
admin.site.register(Order)
admin.site.register(ContactMessage)
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogCategory)


