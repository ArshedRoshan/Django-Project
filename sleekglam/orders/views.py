from locale import currency
from time import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from cart.models import CartItem
from cart.views import checkout
import user
from user.views import login
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct,address,Coupon_applied
import json
from django. conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import razorpay
from user.models import Account
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from xhtml2pdf import pisa 
from adminpanel.models import Coupon,product
from django.contrib import messages



# Create your views here.
# def payment_methods(request,id):
#         current_user = request.user
#         cart_items = CartItem.objects.filter(user=current_user)
#         cart_count = cart_items.count()
#         ad = address.objects.get(id=id)
#         print('address',ad)
#         if cart_count <= 0:
#             return redirect('home')
        
#         total = 0
#         grand_total = 0
#         tax = 0
#         quantity = 0
#         for cart_item in cart_items:
#             total += (cart_item.product.price * cart_item.quantity)
#             quantity += cart_item.quantity
#         tax = (2 * total)/100
#         grand_total = total + tax
        
#         context = {
#                 'order':ad,
#                 'cart_items':cart_items,
#                 'total':total,
#                 'tax':tax,
#                 'grand_total':grand_total,
#         }
    
#         return render(request,'payment.html',context)

  
    
def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    cart_items = CartItem.objects.filter(user=request.user)
    payment= Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],

    )
    payment.save()
    
    order.payment = payment
    order.is_ordered = True
    order.save()
    print("xhgjsc",cart_items)
    # for item in cart_items:
    #     orderproduct = OrderProduct()
    #     print(item.product_id,"product id")
    #     orderproduct.order_id = order.id 
    #     orderproduct.Product= item.product
    #     orderproduct.user_id = request.user.id
    #     orderproduct.quantity = item.quantity
    #     orderproduct.product_price = item.product.price
    #     orderproduct.ordered = True
    #     orderproduct.save() 
    data = {
        'order_number':order.order_number,
        'transID':payment.payment_id,
        
        
    }
    
    
    return JsonResponse(data)

# def payment_razor(request):
#     body = json.loads(request.body)
#     order = Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
#     payment= Payment(
#         user = request.user,
#         payment_id = body['transID'],
#         payment_method = body['payment_method'],
#         amount_paid = order.order_total,
#         status = body['status'],

#     )
#     payment.save()
    
#     order.payment = payment
#     order.is_ordered = True
#     order.save()
    
#     data = {
#         'order_number':order.order_number,
#         'transID':payment.payment_id,
        
        
#     }
    

def add_address(request):
    user = request.user
   
    if request.method == "POST":
      
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            Phone_number = request.POST['Phone_number']
            house = request.POST['house']
            town = request.POST['town']
            locality = request.POST['locality']
            state = request.POST['state']
            country = request.POST['country']
            zip = request.POST['zip']
            add=address.objects.create(user=user,first_name=first_name,last_name=last_name,Phone_number=Phone_number,house=house,town=town,locality= locality,state=state,country=country,zip=zip)
            add.save()

            add = address.objects.filter(user = user)
            
            return redirect('checkout')
         
    else:
        return render(request,'address.html')

def place_order(request,total=0,quantity=0):
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
  
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('home')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
        prod = product.objects.get(id=cart_item.product.id)
        prod.stock = prod.stock-cart_item.quantity
    print('stock',prod.stock)
   
    prod.save()
    tax = (2 * total)/100
    grand_total = total + tax
    
    print(grand_total)
    
    if 'coupon_code' in request.session:
            a = request.session.get('coupon_code')
            print(a)
            coupon = Coupon.objects.get(id=a)
            print('coupon1',coupon)
            z = coupon.discount
            coupon_amount = z
            print('coupon amount',coupon_amount)
            b = (grand_total*coupon_amount)/100
            grand_total = float(grand_total)-b
            print('grand total',grand_total)
            del request.session['coupon_code']
            
    client = razorpay.Client(auth=(settings.KEY,settings.SECRET))
    pay = client.order.create({'amount':int(grand_total*100),'currency':'INR','payment_capture':1})
    print(pay)
    pa = Payment(
    user = request.user,
    payment_id = pay['id'],
    payment_method = 'Razorpay'
    )
    pa.save()
    print("pdhjhhh",pa.id)
    request.session['payment_id']=pa.id
    
    
    
    
    if request.method == 'POST':
            smthg = request.POST.get('address1')
            print('tgrhrh',smthg)
            ad = address.objects.get(id=smthg)
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = ad.first_name
            data.last_name = ad.last_name
            data.phone = ad. Phone_number
            data.address_line_1 = ad.house
            data.address_line_2 = ad.town
            data.country = ad.locality
            data.state = ad.state
            data.city = ad.country
            data.order_note = ad.zip
            data.order_total = grand_total
            data.tax = tax
            z=request.POST.get('payment_method')
            data.payment_method = z
            data.ip = request.META.get('REMOTE_ADDR')
            print(data)
            data.save()
        # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            cart_items = CartItem.objects.filter(user=request.user)
            order = Order.objects.get(user=current_user,is_ordered=False,order_number=data.order_number)
        
            request.session['order_id'] = data.id
        
            for item in cart_items:
                orderproduct = OrderProduct()
                print(item.product_id,"product id")
                orderproduct.order_id = order.id 
                orderproduct.Product= item.product
                orderproduct.user_id = request.user.id
                orderproduct.quantity = item.quantity
                orderproduct.product_price = item.product.price
                orderproduct.ordered = True
                orderproduct.save()
                
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            print('zz',z,type(z))
            y = z == 'COD'
            print('yy',y)
            if y:
                CartItem.objects.filter(user=request.user).delete()
            context = {
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
                'pa':pay
 }
            
            return render(request,'payment.html',context)
            
    return render(request,'checkout.html')

# def cod(request,total=0,quantity=0):
#     current_user = request.user
#     print("order_id in COD",request.session.get('order_id'))
#     order = Order.objects.filter(user=current_user,is_ordered= False)
#     print('order',order)
#     # order_number= order.order_number
#     # print('order number',order_number)


#     cart_items=CartItem.objects.filter(user =current_user)
#     for cart_item in cart_items:
#         total += (cart_item.product.price * cart_item.quantity)
#         quantity += cart_item.quantity
#     tax = (2 * total)/100
#     grand_total = total + tax


#     # if coupon code is present...............
#     if 'coupon_code' in request.session:
#             a = request.session.get('coupon_code')
#             print(a)
#             coupon = Coupon.objects.get(id=a)
#             print('coupon1',coupon)
#             z = coupon.discount
#             coupon_amount = z
#             print('coupon amount',coupon_amount)
#             grand_total = grand_total - coupon_amount
#             print('grand total',grand_total)
            

#     # checking is it cash on delivery
#     if request.method =="POST":
#         order1 = Order.objects.filter(user=current_user,is_ordered= False)
#         paym = request.POST.get('payment_method')
#         print('pay',paym)
#         if paym== "COD":
#             pay= Payment()
#             pay.user = current_user
#             pay.amount_paid = grand_total
#             pay.payment_method = paym
#             pay.status = "success"
#             pay.save()
#             order1.payment = pay
#             order1.is_ordered = True
#             order1.save()
#             # creating an order id for cash on delivery
#             yr = int(datetime.date.today().strftime('%Y'))
#             dt = int(datetime.date.today().strftime('%d'))
#             mt = int(datetime.date.today().strftime('%m'))
#             d = datetime.date(yr, mt, dt)
#             current_date = d.strftime("%Y%m%d")
#             pay_id = current_date + str(pay.id)
#             pay.payment_id=pay_id
#             pay.save()
#             ## moving the cart items into orderproduct table
#             for item in cart_items:
#                 orderprduct = OrderProduct()
#                 orderprduct.order_id = request.session.get('order_id')
#                 orderprduct.payment = pay
#                 orderprduct.user_id = request.user.id
#                 orderprduct.product_id = item.product_id
#                 orderprduct.quantity = item.quantity
#                 orderprduct.product_price = item.product.price
#                 orderprduct.ordered = True
#                 orderprduct.save()
#                 Product = product.objects.get(id = item.product_id)
#                 Product.quantity -= item.quantity
#                 Product.save()
#             # deleting item in cart after order is placed
#             CartItem.objects.filter(user = request.user).delete()
#             return redirect(order_complete)
#         else:
#             return redirect(checkout)
#     order = Order.objects.get(user=current_user, is_ordered=False)
#     # order_number=order_number
#     context = {
#             'order':order,
#             'cart_items':cart_items,
#             'grand_total':grand_total,
#             'tax':tax,
#             'total':total
#             }
#     return render(request,'order_complete',context)








@csrf_exempt
def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    
    try:
        order = Order.objects.get(order_number=order_number,is_ordered = True)
        ordered_products = OrderProduct.objects.filter(order_id = order.id)
        
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity
            
        payment = Payment.objects.get(payment_id = transID)
        
        if 'coupon_code' in request.session:
            a = request.session.get('coupon_code')
            print(a)
            coupon = Coupon.objects.get(id=a)
            print('coupon1',coupon)
            z = coupon.discount
            coupon_amount = z
            print('coupon amount',coupon_amount)
            grand_total = grand_total - coupon_amount
            print('grand total',grand_total)
            del request.session['coupon_code']
        
        if 'coupon_code' in request.session:
            messages.info(request, coupon_amount)
        
        CartItem.objects.filter(user=request.user).delete()
        context = {
            'order':order,
            'ordered_products': ordered_products,
            'order_number':order.order_number,
            'transID': payment.payment_id,
            'payment':payment,
            'subtotal':subtotal
            
        }
        
        return render(request,'order_complete.html',context)
    except (Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('home')
    
    
def order_complete1(request):
    # payment_id=request.session.get('payment_id')
    # order = Order.objects.get(payment=payment_id)
    # ordered_products = OrderProduct.objects.filter(order_id = order.id)
    # payment = Payment.objects.get(payment_id = payment_id)
    
    # subtotal = 0
    # for i in ordered_products:
    #     subtotal += i.product_price * i.quantity
    # 
    
    # context = {
    #         'order':order,
    #         'ordered_products': ordered_products,
    #         'order_number':order.order_number,
    #         'transID': payment.payment_id,
    #         'payment':payment,
    #         'subtotal':subtotal
            
    #     }
    CartItem.objects.filter(user=request.user).delete()
    
    return render(request,'order_complete.html')
    
def invoice_gen(request,id):
    order_data = Order.objects.filter(id=id)

   
    print('order_data',order_data)
    
   
    template_path = 'invoice.html'
    context = {'order_data': order_data}
    

    response = HttpResponse(content_type='application/pdf') #csv file can also be generated using content_type='application/csv
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    
def coupon_code(request):
    if request.user.is_authenticated:
        if request.method == "POST":
                coupon_code = request.POST['coupon']
                print('copon',coupon_code)
                try:
                    coupons = Coupon.objects.get(coupon_code=coupon_code)
                    print("coupon", coupons)

                    if coupons or coupons.active == True:
                        
                        if coupons.user != request.user:
                            print('fsdfs',request.user)
                            request.session['coupon_code'] = coupons.id
                            print('123445',coupons.id)
                            coupons.user = request.user
                            coupons.save()
                            print('kdfdwfdf',coupons)
                            messages.success(request, "coupon is applied")
                            
                        else:
                             messages.error(request, "Not Eligible for coupon")
                    else:
                        messages.error(request, "coupon is invalid")
                except:
                    pass
        return redirect(checkout)
    else:
        return redirect(login)
   
   

# def place_order(request,total=0,quantity=0):
#     current_user = request.user

#     # If the cart count is less than or equal to 0, then redirect back to shop
#     cart_items = CartItem.objects.filter(user=current_user)
#     cart_count = cart_items.count()
#     if cart_count <= 0:
#         return redirect('home')

#     grand_total = 0
#     tax = 0
#     for cart_item in cart_items:
#         total += (cart_item.product.price * cart_item.quantity)
#         quantity += cart_item.quantity
#     tax = (2 * total)/100
#     grand_total = total + tax
    
#     print(grand_total)
    
#     if 'coupon_code' in request.session:
#             a = request.session.get('coupon_code')
#             print(a)
#             coupon = Coupon.objects.get(id=a)
#             print('coupon1',coupon)
#             z = coupon.discount
#             coupon_amount = z
#             print('coupon amount',coupon_amount)
#             grand_total = grand_total - coupon_amount
#             print('grand total',grand_total)
#             del request.session['coupon_code']
            
#     client = razorpay.Client(auth=(settings.KEY,settings.SECRET))
#     pay = client.order.create({'amount':(grand_total*100),'currency':'INR','payment_capture':1})
#     print(pay)
    
    
    
#     pa = Payment(
#     user = request.user,
#     payment_id = pay['id']
#     )
#     pa.save()
    

#     if request.method == 'POST':
#             smthg = request.POST.get('address1')
#             print('tgrhrh',smthg)
#             ad = address.objects.get(id=smthg)
#             # Store all the billing information inside Order table
#             data = Order()
#             data.user = current_user
#             data.first_name = ad.first_name
#             data.last_name = ad.last_name
#             data.phone = ad. Phone_number
#             data.address_line_1 = ad.house
#             data.address_line_2 = ad.town
#             data.country = ad.locality
#             data.state = ad.state
#             data.city = ad.country
#             data.order_note = ad.zip
#             data.order_total = grand_total
#             data.tax = tax
#             z=request.POST.get('payment_method')
#             data.payment_method = z
#             data.ip = request.META.get('REMOTE_ADDR')
#             print(data)
#             data.save()
#         # Generate order number
#             yr = int(datetime.date.today().strftime('%Y'))
#             dt = int(datetime.date.today().strftime('%d'))
#             mt = int(datetime.date.today().strftime('%m'))
#             d = datetime.date(yr,mt,dt)
#             current_date = d.strftime("%Y%m%d") #20210305
#             order_number = current_date + str(data.id)
#             data.order_number = order_number
#             data.save()
#             cart_items = CartItem.objects.filter(user=request.user)
#             order = Order.objects.get(user=current_user,is_ordered=False,order_number=data.order_number)
        
#             request.session['order_id'] = data.id
        
#             for item in cart_items:
#                 orderproduct = OrderProduct()
#                 print(item.product_id,"product id")
#                 orderproduct.order_id = order.id 
#                 orderproduct.Product= item.product
#                 orderproduct.user_id = request.user.id
#                 orderproduct.quantity = item.quantity
#                 orderproduct.product_price = item.product.price
#                 orderproduct.ordered = True
#                 orderproduct.save()
                
#             order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
#             print('zz',z,type(z))
#             y = z == 'COD'
#             print('yy',y)
#             if y:
#                 CartItem.objects.filter(user=request.user).delete()
#             context = {
#                 'order':order,
#                 'cart_items':cart_items,
#                 'total':total,
#                 'tax':tax,
#                 'grand_total':grand_total,
#                 'pa':pay
#  }
            
#             return render(request,'payment.html',context)
            
#     return render(request,'checkout.html')