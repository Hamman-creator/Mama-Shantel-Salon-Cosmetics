from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from .models import CustomUser,Order,Booking


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

User = get_user_model()

class UpdateAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number']


class GuestOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'guest_name', 'guest_contact']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'guest_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guest_contact': forms.TextInput(attrs={'class': 'form-control'}),
        }


class GuestBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['hairstyle', 'preferred_date', 'guest_name', 'guest_contact']
        widgets = {
            'hairstyle': forms.Select(attrs={'class': 'form-control'}),
            'preferred_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'guest_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guest_contact': forms.TextInput(attrs={'class': 'form-control'}),
        }


class GuestCheckoutForm(forms.Form):
    guest_name = forms.CharField(max_length=100)
    guest_contact = forms.CharField(max_length=100)
    guest_location = forms.CharField(max_length=255, required=False)
    preferred_time = forms.TimeField(required=True, widget=forms.TimeInput(attrs={'type': 'time'}))
