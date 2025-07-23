from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.custom_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/bookings/', views.user_bookings_view, name='user_bookings'),
    path('dashboard/orders/', views.user_orders_view, name='user_orders'),
    path('dashboard/update/', views.update_account, name='update_account'),
    path('', views.landing_page, name='landing'),
    path('products/', views.products_page, name='products'),
    path('hairs/', views.hairs_page, name='hairs'),
    path('contact/', views.contact_view, name='contact'),
    path('products/', views.products_page, name='product_gallery'),
    path('add-to-cart/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('confirm-cart/', views.confirm_cart, name='confirm_cart'),
    path('guest/book-hairstyle/<int:hairstyle_id>/', views.guest_book_hairstyle, name='guest_book_hairstyle'),
    path('guest/order-product/<int:product_id>/', views.guest_order_product, name='guest_order_product'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

]


