from ast import pattern
from django.urls import path
from .import views

urlpatterns = [
    path('wishlist/',views.wish,name='wish_list'),
    path('add_wish_list/<int:product_id>/',views.add_wish_list,name='add_wish_list'),
    path('remove_wish/<int:product_id>/<int:wish_item_id>/',views.remove_wish,name='remove_wish'),
   path('remove_wish_item/<int:product_id>/',views.remove_wish_item,name='remove_wish_item'),
]