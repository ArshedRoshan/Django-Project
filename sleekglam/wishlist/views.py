from django.shortcuts import render

# Create your views here.
from gc import get_objects
from site import check_enableusersite
from django.shortcuts import render,redirect,get_object_or_404
from adminpanel . models import product
from . models import Wish,WishItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


# Create your views here.

def _wish_id(request):
    wish = request.session.session_key
    if not wish:
        wish = request.session.create()
    return wish


def add_wish_list(request, product_id):
    Product = product.objects.get(id=product_id)
    try:
        wish = Wish.objects.get(wish_id=_wish_id(request))
    except Wish.DoesNotExist:
        wish  = Wish.objects.create(
            wish_id = _wish_id(request)
        )
    wish.save()
    
    try:
        wish_item = WishItem.objects.get(product = Product,wish = wish)
        wish_item.quantity +=1
        wish_item.save()
    except WishItem.DoesNotExist:
        wish_item = WishItem.objects.create(
            product = Product,
            quantity = 1,
            wish = wish,
        )
        wish_item.save()
  
   
    return redirect('wish_list')

def remove_wish(request,product_id,cart_item_id):
    
    Product = get_object_or_404(product,id=product_id)
    try:
        if request.user.is_authenticated:
             wish_item = WishItem.objects.get(product = Product,user=request.user,id=cart_item_id)
        else:
            wish = Wish.objects.get(wish_id=_wish_id(request))
            wish_item = WishItem.objects.get(product = Product,wish = wish)
        if wish_item.quantity > 1:
            wish_item.quantity -= 1
            wish_item.save()
        else:
          wish_item.delete()
    except:
        pass
    return redirect('whish_list')

def remove_wish_item(request,product_id):
    Product = get_object_or_404(product,id=product_id)
    if request.user.is_authenticated:
        wish_item = WishItem.objects.filter(product = Product,user=request.user) 
    else:
      wish = Wish.objects.get(wish_id=_wish_id(request))
      wish_item = WishItem.objects.filter(product = Product,wish = wish) 
    wish_item.delete()
    return redirect('wish_list')
        


def wish(request,total=0,quantity=0,wish_items=None):
  
    
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
           wish_items = WishItem.objects.filter(user=request.user,is_active=True)
        else: 
            wish=Wish.objects.get(wish_id=_wish_id(request))
            wish_items = WishItem.objects.filter(wish=wish,is_active=True)
        
        for wish_item in wish_items:
            total = (wish_item.product.price * wish_item.quantity)+total
            quantity = wish_item.quantity+quantity
        tax = (2*total)/100
        # discount = total-2
        grand_total = (total + tax)
       
    except ObjectDoesNotExist:
        pass
    context = {
        'total':total,
        'quantity':quantity,
        'wish_items':wish_items,
        'tax':tax,
        'grand_total':grand_total,
        # 'discount':discount
        }
            
    return render(request,'wishlist.html',context)
