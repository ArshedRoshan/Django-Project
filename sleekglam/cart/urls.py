from ast import pattern
from django.urls import path
from .import views

urlpatterns = [
    path('cart',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',views.remove_cart,name='remove_cart'),
    path('remove_cart_item/<int:product_id>/',views.remove_cart_item,name='remove_cart_item'),
    
    path('cart/checkout/',views.checkout,name='checkout'),
    path('minus/<int:product_id>/<int:cart_item_id>',views.minus,name='minus'),
    path('plus/<int:product_id>/<int:cart_item_id>',views.plus,name='plus'),
]
