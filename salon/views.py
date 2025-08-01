from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from salon.forms import CustomUserCreationForm, UpdateAccountForm, GuestCheckoutForm
from django.contrib.auth.decorators import login_required
from .models import Booking, Order,ContactMessage,Product,Hairstyle,CartItem,ProductCategory,HairstyleCategory
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_time
from django.core.paginator import Paginator


def landing_page(request):
    return render(request, 'landing.html') 

 # Make sure Category is imported




def products_page(request):
    category_id = request.GET.get('category')
    page_size = int(request.GET.get('page_size', 8))  # Default 8 if not provided
    page_number = request.GET.get('page')

    products = Product.objects.all()
    if category_id:
        products = products.filter(category_id=category_id)

    paginator = Paginator(products, page_size)
    page_obj = paginator.get_page(page_number)

    categories = ProductCategory.objects.all()

    return render(request, 'products.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
    })


def hairs_page(request):
    category_id = request.GET.get('category')
    page_size = int(request.GET.get('page_size', 8))  # Default 8 if not provided
    page_number = request.GET.get('page')

    hairstyles = Hairstyle.objects.all()
    if category_id:
        hairstyles = hairstyles.filter(category_id=category_id)

    paginator = Paginator(hairstyles, page_size)
    page_obj = paginator.get_page(page_number)

    categories = HairstyleCategory.objects.all()

    return render(request, 'hair.html', {
        'hairstyles': hairstyles,
        'categories': categories,
        'selected_category': category_id,
    })



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

    total_bookings = bookings.count()
    total_orders = orders.count()

    # Add status-based counts
    pending_bookings = bookings.filter(status='Pending').count()
    completed_bookings = bookings.filter(status='Completed').count()

    pending_orders = orders.filter(status='Pending').count()
    completed_orders = orders.filter(status='Completed').count()

    return render(request, 'salon/dashboard.html', {
        'bookings': bookings,
        'orders': orders,
        'total_bookings': total_bookings,
        'total_orders': total_orders,
        'pending_bookings': pending_bookings,
        'completed_bookings': completed_bookings,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
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

    if request.method == 'POST':
        print("==== POST received ====")
        for item in items:
            location = request.POST.get(f'location_{item.id}')
            preferred_date = request.POST.get(f'preferred_date_{item.id}')
            time = request.POST.get(f'time_{item.id}')

            if location:
                item.guest_location = location
            if preferred_date:
                item.preferred_date = preferred_date
            if time:
                item.time = time
            item.save()

        return redirect('confirm_cart')

    return render(request, 'salon/cart.html', {'items': items})





from .utils import get_or_create_session_key
from django.utils.dateparse import parse_date, parse_time
from .models import CartItem, Order, Booking
from .forms import GuestCheckoutForm
from django.shortcuts import render, redirect


def confirm_cart(request):
    session_key = get_or_create_session_key(request)
    items = CartItem.objects.filter(user=request.user) if request.user.is_authenticated else CartItem.objects.filter(session_key=session_key)

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
        # Update fields
        for item in items:
            if item.product:
                location_value = request.POST.get(f'location_{item.id}')
                if location_value:
                    item.guest_location = location_value
            elif item.hairstyle:
                date_val = request.POST.get(f'preferred_date_{item.id}')
                time_val = request.POST.get(f'time_{item.id}')
                if date_val:
                    item.preferred_date = parse_date(date_val)
                if time_val:
                    item.time = parse_time(time_val)
            item.save()

        if request.user.is_authenticated:
            for item in items:
                if item.product:
                    Order.objects.create(
                        customer=request.user,
                        product=item.product,
                        quantity=item.quantity,
                        is_guest=False
                    )
                elif item.hairstyle:
                    Booking.objects.create(
                        customer=request.user,
                        hairstyle=item.hairstyle,
                        preferred_date=item.preferred_date,
                        time=item.time,
                        is_guest=False
                    )
        else:
            form = GuestCheckoutForm(request.POST)
            if form.is_valid():
                guest_name = form.cleaned_data['guest_name']
                guest_contact = form.cleaned_data['guest_contact']
                for item in items:
                    if item.product:
                        Order.objects.create(
                            customer=None,
                            product=item.product,
                            quantity=item.quantity,
                            is_guest=True,
                            guest_name=guest_name,
                            guest_contact=guest_contact,
                            guest_location=item.guest_location
                        )
                    elif item.hairstyle:
                        Booking.objects.create(
                            customer=None,
                            hairstyle=item.hairstyle,
                            preferred_date=item.preferred_date,
                            time=item.time,
                            is_guest=True,
                            guest_name=guest_name,
                            guest_contact=guest_contact
                        )
            else:
                return render(request, 'salon/confirm_cart.html', {
                    'items': items,
                    'form': form,
                    'total_price': total_price,
                    'total_items': total_items,
                })

        items.delete()
        if request.user.is_authenticated:
            return redirect('dashboard')  # Replace with your actual dashboard URL name
        else:
            return redirect('thank_you')

    else:
        form = GuestCheckoutForm() if not request.user.is_authenticated else None

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



def thank_you(request):
    return render(request, 'salon/thank_you.html')





# def product_gallery(request):
#     products = Product.objects.all()
#     return render(request, 'products.html', {'products': products})

# def hairstyle_gallery(request):
#     hairstyles = Hairstyle.objects.all()
#     return render(request, 'hair.html', {'hairs': hairstyles})


