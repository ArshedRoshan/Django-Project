from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
     path('place_order', views.place_order, name='place_order'),
     path('payments',views.payments,name='payments'),
     path('ordercomplete',views.order_complete,name='order_complete'),
     # path('cod',views.cod,name='cod'),
     # path('payment_methods/<int:id>',views.payment_methods,name='payment_methods'),
     
     
     path('add_address',views.add_address,name='add_address'),
     path('invoice_gen/<int:id>',views.invoice_gen,name='invoice_gen'),
     path('coupon_code',views.coupon_code,name='coupon_code'),
     path('ordercomplete1',views.order_complete1,name='order_complete1'),

]