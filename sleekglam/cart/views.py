from email import message
from gc import get_objects
from django.contrib import messages,auth
from site import check_enableusersite
from django.shortcuts import render,redirect,get_object_or_404
from adminpanel . models import product
from adminpanel.models import Coupon
from user import *
from . models import Cart,CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from orders.models import address


# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    #get the product
    # If the user is authenticated
    Product= product.objects.get(id=product_id)
    if request.user.is_authenticated:
        try:
            cart= Cart.objects.get(cart_id =_cart_id(request))
        except:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
            cart.save()
        try:
            cart_item = CartItem.objects.get(product=Product,cart=cart,user=request.user)
            if cart_item.quantity <10:
                cart_item.quantity += 1 #pressing first time cart button
                cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=Product,
                quantity=1,
                user=request.user,
                cart=cart,
            )
            cart_item.save()       
    else:
    
        try:    
                print('t')
                cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
                print('l')
                cart = Cart.objects.create(
                    cart_id = _cart_id(request)
                )
        cart.save()

        try: 
            print('s')
            cart_item=CartItem.objects.get(product=Product,cart=cart)
            if cart_item.quantity <10:
                cart_item.quantity += 1 #pressing first time cart button
                cart_item.save()
        except CartItem.DoesNotExist:
            print('y')
            cart_item=CartItem.objects.create(product=Product,quantity=1,cart=cart,)
            cart_item.save()

        
    return redirect('cart')
       
    

def remove_cart(request,product_id,cart_item_id):
    
    Product = get_object_or_404(product,id=product_id)
    try:
        if request.user.is_authenticated:
             cart_item = CartItem.objects.get(product = Product,user=request.user,id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product = Product,cart = cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
          cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request,product_id):
    Product = get_object_or_404(product,id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.filter(product = Product,user=request.user) 
    else:
      cart = Cart.objects.get(cart_id=_cart_id(request))
      cart_item = CartItem.objects.filter(product = Product,cart = cart) 
    cart_item.delete()
    return redirect('cart')
        
        
        

def cart(request,total=0,quantity=0,cart_items=None):    
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            print(cart_items)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore
    
   
    
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        # 'discount':discount
        }
            
    return render(request,'cart.html',context)

def minus(request, product_id, cart_item_id):

    Product = get_object_or_404(product, id=product_id)
    
    if request.user.is_authenticated:
            print('helloo')
            cart_item = CartItem.objects.get(product=Product, user=request.user, id=cart_item_id)
    else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=Product, cart=cart, id=cart_item_id)
    if cart_item.quantity > 1:
            print('decrement')

            cart_item.quantity -= 1
            cart_item.save()
            print(cart_item.quantity)
            return HttpResponse(cart_item.quantity)
    

    return HttpResponse(1)        

       

def plus(request, product_id, cart_item_id):

    Product = get_object_or_404(product, id=product_id) 
    
    if request.user.is_authenticated:
            print('hellooyy')
            cart_item = CartItem.objects.get(product=Product, user=request.user, id=cart_item_id)
    else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=Product, cart=cart, id=cart_item_id)
    if cart_item.quantity < 10 :
            print('increment')

            cart_item.quantity += 1
            cart_item.save()
            print(cart_item.quantity)
            return HttpResponse(cart_item.quantity)


    return HttpResponse(10)




@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_items=None):
        try:
          tax = 0
          grand_total = 0
          if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
            
          for cart_item in cart_items:
              total = (cart_item.product.price * cart_item.quantity)+total
              quantity = cart_item.quantity+quantity
          tax = (2*total)/100
            # discount = total-2
          grand_total = (total + tax)
        
        except ObjectDoesNotExist:
            pass
        
        add = address.objects.filter(user=request.user)
        print('ggdfg',add)
        if 'coupon_code' in request.session:
            a = request.session.get('coupon_code')
            print(a)
            coupon = Coupon.objects.get(id=a)
            print('coupon1',coupon)
            z = coupon.discount
            coupon_amount = z
            print('coupon amount',coupon_amount)
            b = (grand_total*coupon_amount)/100
            grand_total = grand_total-b
            
        
        if 'coupon_code' in request.session:
            messages.info(request, coupon_amount)
        
        context = {
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
            'tax':tax,
            'grand_total':grand_total,
            # 'discount':discount
            'add':add,
            
            }
        return render(request,'checkout.html',context)


    