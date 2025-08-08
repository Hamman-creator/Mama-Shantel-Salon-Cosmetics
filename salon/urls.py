from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.custom_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/bookings/', views.user_bookings_view, name='user_bookings'),
    path('dashboard/orders/', views.user_orders_view, name='user_orders'),
    path('dashboard/update/', views.update_account, name='update_account'),
    path('', views.landing_page, name='landing'),
    path('submit-review/', views.submit_review, name='submit_review'),
    path('reviews/', views.all_reviews_page, name='all_reviews'),
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
    path('thank-you/', views.thank_you, name='thank_you'),
        # password reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='salon/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='salon/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='salon/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='salon/password_reset_complete.html'), name='password_reset_complete'),
    
    path('terms/', TemplateView.as_view(template_name='terms.html'), name='terms'),


    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'), 

]


