from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings 
from django.contrib.auth import get_user_model
# Extended user profile
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']  # if you still want username as a required field


    def __str__(self):
        return self.username

# Categories for Products
class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Products
class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name

# Categories for Hairstyles
class HairstyleCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Hairstyles
class Hairstyle(models.Model):
    category = models.ForeignKey(HairstyleCategory, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='hairstyles/')

    def __str__(self):
        return self.name

# Booking
class Booking(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    hairstyle = models.ForeignKey(Hairstyle, on_delete=models.CASCADE)
    preferred_date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    date_booked = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Pending")
    
    guest_name = models.CharField(max_length=100, blank=True, null=True)
    guest_contact = models.CharField(max_length=100, blank=True, null=True)  # Phone
    guest_email = models.EmailField(blank=True, null=True)
    guest_location = models.CharField(max_length=255, blank=True, null=True)

    
    is_guest = models.BooleanField(default=False)

    def __str__(self):
        if self.customer:
         return f"{self.customer.username} - {self.hairstyle.name}"
        return f"Guest - {self.hairstyle.name}"

# Product Order
class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Pending")
    
    guest_name = models.CharField(max_length=100, blank=True, null=True)
    guest_contact = models.CharField(max_length=100, blank=True, null=True)  # Phone
    guest_email = models.EmailField(blank=True, null=True)
    guest_location = models.CharField(max_length=255, blank=True, null=True)

    
    is_guest = models.BooleanField(default=False)

    def __str__(self):
        if self.customer:
            return f"{self.customer.username} - {self.product.name}"
        return f"Guest - {self.product.name}"




class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


#cartitems 
class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    hairstyle = models.ForeignKey(Hairstyle, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time = models.TimeField(null=True, blank=True)  # 👈 Add this line
    added_at = models.DateTimeField(auto_now_add=True)
    # is_guest = models.BooleanField(default=False)

    guest_name = models.CharField(max_length=100, blank=True, null=True)
    guest_contact = models.CharField(max_length=100, blank=True, null=True)
    guest_email = models.EmailField(blank=True, null=True)
    guest_location = models.CharField(max_length=255, blank=True, null=True)

    time = models.TimeField(null=True, blank=True)