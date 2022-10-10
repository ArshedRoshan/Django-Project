from unicodedata import name
from django.contrib import admin
from django.urls import path
from .import views


urlpatterns = [
    path('',views.home,name='home'),
    path('home1',views.home1,name='home1'),
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('otp',views.otplogin,name='otp'),
    path('otp_login',views.otp_login,name='otp_login'),
    path('product_detail/<int:id>',views.ProductDetail,name='product_detail'),
    path('men/<id>',views.mens,name='men'),
    path('category',views.category,name='category'),

    
    path('my_orders/',views.my_orders,name='my_orders'),
    path('order_details/<int:order_id>/',views.order_detail,name='order_detail'),
    path('cancel_order/<int:order_id>',views.cancel_order,name='cancel_order'),
    path('return_order/<int:id>',views.return_order,name='return_order'),
    path('forgotpassword',views.forgotpassword,name="forgotpassword"),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'),
    
    
    path('my_profile',views.my_profile,name='my_profile'),
    path('edit_profile/<int:id>',views.edit_profile,name='edit_pro'),
    path('change_password',views.change_password,name='change_password'),
    path('profile_order_delete/<int:id>',views.profile_order_delete,name='profile_order_delete'),
    path('wallet',views.wallets,name='wallets'),
    
      
]