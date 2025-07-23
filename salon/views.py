from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from salon.forms import CustomUserCreationForm, UpdateAccountForm, GuestCheckoutForm
from django.contrib.auth.decorators import login_required
from .models import Booking, Order,ContactMessage,Product,Hairstyle,CartItem 
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone


def landing_page(request):
    return render(request, 'landing.html') 

def products_page(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def hairs_page(request):
    hairstyles = Hairstyle.objects.all()
    return render(request, 'hair.html', {'hairstyles': hairstyles})

def custom_login(request): 
    if request.method == 'POST':
        phone_number = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'salon/login.html', {'error': 'Invalid credentials'})
    return render(request, 'salon/login.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'salon/signup.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-date_booked')
    orders = Order.objects.filter(customer=request.user).order_by('-date_ordered')
    return render(request, 'salon/dashboard.html', {
        'bookings': bookings,
        'orders': orders,
    })

@login_required
def user_bookings_view(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-date_booked')
    return render(request, 'salon/bookings.html', {'bookings': bookings})

@login_required
def user_orders_view(request):
    orders = Order.objects.filter(customer=request.user).order_by('-date_ordered')
    return render(request, 'salon/orders.html', {'orders': orders})

@login_required
def update_account(request):
    user = request.user

    if request.method == 'POST':
        form = UpdateAccountForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user, request.POST)

        if form.is_valid() and password_form.is_valid():
            form.save()
            password_form.save()
            update_session_auth_hash(request, password_form.user)  # Keeps user logged in
            return redirect('update_account')
    else:
        form = UpdateAccountForm(instance=user)
        password_form = PasswordChangeForm(user)

    return render(request, 'salon/update_account.html', {
        'form': form,
        'password_form': password_form,
    })



@login_required
def book_hairstyle(request, hairstyle_id):
    
    if request.method == 'POST':
        preferred_date = request.POST['preferred_date']
        time = request.POST['time']
        Booking.objects.create(
            customer=request.user,
            hairstyle_id=hairstyle_id,
            preferred_date=preferred_date,
            time=time,
            date_booked=timezone.now()
        )
        return redirect('dashboard')
    return render(request, 'salon/book_hairstyle.html')


def guest_book_hairstyle(request, hairstyle_id):
    if request.method == 'POST':
        preferred_date = request.POST['preferred_date']
        time = request.POST['time']
        guest_name = request.POST['guest_name']
        guest_contact = request.POST['guest_contact']
        Booking.objects.create(
            customer=None,
            hairstyle_id=hairstyle_id,
            preferred_date=preferred_date,
            time=time,
            date_booked=timezone.now(),
            is_guest=True,
            guest_name=guest_name,
            guest_contact=guest_contact
        )
        return redirect('landing')
    return render(request, 'salon/guest_book.html')

@login_required
def order_product(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        Order.objects.create(
            customer=request.user,
            product_id=product_id,
            quantity=quantity,
            date_ordered=timezone.now()
        )
        return redirect('dashboard')
    


def guest_order_product(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        guest_name = request.POST['guest_name']
        guest_contact = request.POST['guest_contact']
        Order.objects.create(
            customer=None,
            product_id=product_id,
            quantity=quantity,
            date_ordered=timezone.now(),
            is_guest=True,
            guest_name=guest_name,
            guest_contact=guest_contact
        )
        return redirect('landing')
    return render(request, 'salon/guest_order.html')



def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        return render(request, 'contact_success.html')  # or redirect to thank-you page

    return render(request, 'contact.html')


def get_or_create_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def add_to_cart(request, item_type, item_id):
    session_key = get_or_create_session_key(request)
    preferred_date = request.POST.get('preferred_date')
    redirect_target = request.GET.get('redirect', 'gallery')
    if item_type == 'product':
        product = Product.objects.get(id=item_id)
        CartItem.objects.create(user=request.user if request.user.is_authenticated else None,
                                session_key=None if request.user.is_authenticated else session_key,
                                product=product)
    elif item_type == 'hairstyle':
        style = Hairstyle.objects.get(id=item_id)
        CartItem.objects.create(user=request.user if request.user.is_authenticated else None,
                                session_key=None if request.user.is_authenticated else session_key,
                                hairstyle=style,
                                preferred_date=preferred_date)
        


    if not request.user.is_authenticated:
        return redirect('view_cart')
    
    if redirect_target == 'checkout':
        return redirect('confirm_cart')
    elif redirect_target == 'products':
        return redirect('products')  
    elif redirect_target == 'hairs':
        return redirect('hairs')     

    return redirect('view_cart' if request.user.is_authenticated else 'hairs')


def view_cart(request):
    session_key = get_or_create_session_key(request)
    
    if request.user.is_authenticated:
        items = CartItem.objects.filter(user=request.user)
    else:
        items = CartItem.objects.filter(session_key=session_key)

    return render(request, 'salon/cart.html', {'items': items})


def confirm_cart(request):
    session_key = get_or_create_session_key(request)
    items = CartItem.objects.filter(user=request.user) if request.user.is_authenticated else CartItem.objects.filter(session_key=session_key)

    # === Calculate total price and total item count ===
    total_price = 0
    total_items = 0
    for item in items:
        if item.product:
            total_price += item.product.price * item.quantity
            total_items += item.quantity
        elif item.hairstyle:
            total_price += item.hairstyle.price
            total_items += 1

    if request.method == 'POST':
        form = GuestCheckoutForm(request.POST) if not request.user.is_authenticated else None

        if request.user.is_authenticated or (form and form.is_valid()):
            guest_name = form.cleaned_data['guest_name'] if form else None
            guest_contact = form.cleaned_data['guest_contact'] if form else None

            for item in items:
                if item.product:
                    Order.objects.create(
                        customer=request.user if request.user.is_authenticated else None,
                        product=item.product,
                        quantity=item.quantity,
                        is_guest=not request.user.is_authenticated,
                        guest_name=guest_name,
                        guest_contact=guest_contact
                    )
                elif item.hairstyle:
                    Booking.objects.create(
                        customer=request.user if request.user.is_authenticated else None,
                        hairstyle=item.hairstyle,
                        preferred_date=item.preferred_date,
                        is_guest=not request.user.is_authenticated,
                        guest_name=guest_name,
                        guest_contact=guest_contact
                    )
            items.delete()
            return redirect('dashboard')  # You can redirect to a thank-you page instead

    else:
        form = GuestCheckoutForm() if not request.user.is_authenticated else None

    # === Pass totals to the template ===
    return render(request, 'salon/confirm_cart.html', {
        'items': items,
        'form': form,
        'total_price': total_price,
        'total_items': total_items,
    })





def remove_from_cart(request, item_id):
    session_key = get_or_create_session_key(request)

    try:
        if request.user.is_authenticated:
            item = CartItem.objects.get(id=item_id, user=request.user)
        else:
            item = CartItem.objects.get(id=item_id, session_key=session_key)
        item.delete()
    except CartItem.DoesNotExist:
        pass  # silently ignore errors

    return redirect('view_cart')




# def product_gallery(request):
#     products = Product.objects.all()
#     return render(request, 'products.html', {'products': products})

# def hairstyle_gallery(request):
#     hairstyles = Hairstyle.objects.all()
#     return render(request, 'hair.html', {'hairs': hairstyles})


