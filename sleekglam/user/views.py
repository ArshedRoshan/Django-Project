from contextvars import Context
import datetime
import email
from http import client
from multiprocessing import context
import profile
from django.contrib import messages,auth
from django.shortcuts import render
from django.shortcuts import render,redirect,reverse,get_object_or_404
from orders.models import OrderProduct
from orders.models import address
from .models import Account, Profile,referal,wallet
import random
from twilio.rest import Client
from adminpanel.models import categories,banner,cat_offer,product_offer
from django.contrib.auth import authenticate
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.contrib.auth.decorators import login_required
from cart . models import*
from cart .views import _cart_id
from .forms import RegistrationForm
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.db.models import Q
import requests
from orders . models import Order
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator  
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
import string
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import get_template
from xhtml2pdf import pisa 

# Create your views here.
def home(request):
    
    #   products = product.objects.filter(is_active=1)
    #   context = {
    #     'products':products,
    # }
    return redirect(category)
    #   return render(request,'home.html',context)

def home1(request):
    
      products = product.objects.filter(is_active=1)
      context = {
        'products':products,
    }
    
      return render(request,'home1.html',context)
  
def signup(request):
     form= RegistrationForm()
     if request.method == 'POST':
          form = RegistrationForm(request.POST)
          if form.is_valid():
              first_name = form.cleaned_data['first_name']
              last_name = form.cleaned_data['last_name']
              email = form.cleaned_data['email']
              phone_number= form.cleaned_data['phone_number']
              password = form.cleaned_data['password']
              username = email.split("@")[0]
              user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
              user.phone_number = phone_number
              user.save()
              
              random_code = get_random_string(7, allowed_chars=string.ascii_uppercase + string.digits)
              refer = referal()
              refer.referal_code = random_code
              print("referal code",refer.referal_code)
              refer.user = user
              refer.save()
                
              messages.success(request,'Registration SucessFull')
              return redirect('login')
          else:
              form= RegistrationForm()
     
     context = {
         'form':form
     }
     
     return render(request,'signup.html',context)
        

   
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email)
        print(password)
        
        user = auth.authenticate(username=email,password=password)
        print(user)
        
        if user is not None:
            
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request,user)
            messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                print('query',query)
                params = dict(x.split('=') for x in query.split('&'))
                print('params',params)
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
        
        if user:
            obj = Account.objects.get(username=email)
            if obj.status is True:
                messages.warning(request,"You are blocked")
                return redirect('login')
        
           
            
            
    return render(request, 'login.html')

  
def logout(request):
     auth.logout(request)
     messages.success(request,'You are logged out')
     return redirect('home')
  
# def otplogin(request):
#     if request.method == 'POST':
#         otp = request.POST.get('otp')
#         a=Account.objects.filter(phone_number=otp)
#         if a:
#             # otp=2255
#             otp = random.randint(1000,9999)
#             account_sid = "AC6519f2b3de98ced2e2ae204d783a2a44"
#             auth_token = "ff669a2a7fa0a0b58cb012be8a86ca07"
#             client = Client(account_sid,auth_token)
#             msg = client.messages.create(
#                 body = f"Your OTP is {otp}",
#                 from_ = "+19594568608",
#                 to = "+917510768809"
#             )

#             request.session['otp'] = otp
#             return redirect('otp_login')
#         else:
#             return redirect('signup')
#     return render(request,'phone.html')
            
    

# def otp_login(request):
#     if request.method == 'POST':
#         otp = request.POST.get('otp')
#         otpp = request.session.get('otp')
#         print(otp,otpp)
#         print(type(otp),type(otpp))
#         if int(otp) == otpp:
#             return redirect('home')
#     return render(request,'otp.html')


def otp_login(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        print(otp)
        phone_no = request.session['phone_no']
        print(phone_no)
        if Account.objects.filter(phone_number =phone_no).exists():
            user = Account.objects.get(phone_number =phone_no)
            print('user',user)
            
            account_sid = "AC6519f2b3de98ced2e2ae204d783a2a44"
            auth_token = "ff669a2a7fa0a0b58cb012be8a86ca07"
            client = Client(account_sid,auth_token)
            verification_check = client.verify \
                .services("VAb8cae8e9f95e6f86522a4010138356dd") \
                .verification_checks \
                .create(to='+91'+phone_no, code=otp)
            if verification_check.status == "approved":
                auth.login(request,user)
                request.session['customer'] = request.session.get('phone')
                return redirect('/')
            else:
                messages.info(request,'invalid OTP')
                return render(request, 'phone.html')
        else:
            messages.warning(request, 'invalid phone number')
            return render(request, 'phone.html')
    else:
        return render(request, 'otp.html')








def otplogin(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        request.session['phone'] = phone

        if Account.objects.filter(phone_number=phone).exists():
            # totp= pyotp.TOTP('base32secret3232').now()
            request.session['phone_no'] = phone

            otp = random.randint(1000,9999)
            account_sid = "AC6519f2b3de98ced2e2ae204d783a2a44"
            auth_token = "ff669a2a7fa0a0b58cb012be8a86ca07"
            client = Client(account_sid,auth_token)
            verification = client.verify \
                .services("VAb8cae8e9f95e6f86522a4010138356dd") \
                .verifications \
                .create(to='+91'+phone, channel='sms')
            

            return redirect(otp_login)
        else:

            messages.info(request, "invalid number")
            return render(request, 'phone.html')
    else:
        return render(request, 'phone.html')

def category(request):
        category = categories.objects.all()
        products = product.objects.filter(is_active=1)
        Banner = banner.objects.all()
        
        cat_off = cat_offer.objects.all()
        pro =  product_offer.objects.all()
        

        p = product.objects.all()
        for i in p:
            i.price=i.dicscount_price
            print('price',i.productname,i.price)
            print('s_price',i.dicscount_price)
            i.save()
        now=datetime.datetime.now().strftime('%Y-%m-%d')
        print(now)
        products = product.objects.all()
        
        for k in products:
            try: 
               p_offer=product_offer.objects.get(valid_from__lte=now,valid_to__gte=now,Product=k.id)
               print('svszvs',p_offer)
               print('Hello outter try')
               try:
                  c_offer=cat_offer.objects.get(valid_from__lte=now,valid_to__gte=now,category=k.categories)
                  print('Hello Inner try')
                  if int(p_offer.offer_amount) > int(c_offer.discount_amount):
                        print("p_offer.discount_percentage > c_offer.discount_percentage",p_offer.offer_amount,c_offer.discount_amount)
                        calculating_discount=p_offer.offer_amount*int(k.dicscount_price)/100
                        k.price=int(k.dicscount_price)-calculating_discount
                        k.save()
                  elif int(p_offer.offer_amount) < int(c_offer.discount_amount):
                        print("p_offer.offer_amount< c_offer.discount_amount",p_offer.offer_amount,c_offer.discount_amount)
                        calculating_discount=c_offer.discount_amount*int(k.dicscount_price)/100
                        k.price=int(k.dicscount_price)-calculating_discount
                        k.save()
                  elif int(p_offer.offer_amount) == int(c_offer.discount_amount):
                        print("p_offer.offer_amount == c_offer.discount_amount",p_offer.offer_amount,c_offer.discount_amount)
                        calculating_discount=p_offer.offer_amount*int(k.dicscount_price)/100
                        k.price=int(k.dicscount_price)-calculating_discount
                        k.save()
               except:
                     p_offer=product_offer.objects.get(valid_from__lte=now,valid_to__gte=now,Product=k.id)
                     calculating_discount=p_offer.offer_amount*int(k.dicscount_price)/100
                     k.price=int(k.dicscount_price)-calculating_discount
                     k.save()
            except:
                    try:
                      print('hello 2nd try')
                      c_offer=cat_offer.objects.get( valid_from__lte=now,valid_to__gte=now,category=k.categories)
                      calculating_discount=c_offer.discount_amount*int(k.dicscount_price)/100
                      k.price=int(k.dicscount_price)-calculating_discount
                      k.save()
                    except:
                           pass
                     
                
                        
            
        
        
        
        
        
        # category_offer= cat_offer.objects.filter( valid_from__lte=now,valid_to__gte=now)
        
        category_offer1 = cat_offer.objects.all()
        product_offer1 = product_offer.objects.all()
        
        # print('fsdfs',category_offer)
        # if category_offer:
        #     for i in category_offer:
        #         apply_category_product=product.objects.filter(categories = i.category)
        #         print('apply',apply_category_product)
        #     for j in apply_category_product:
        #             j.price=(float(j.dicscount_price)*float(i.discount_amount))/100
        #             j.save()   
            
        # if  product_offer.objects.filter(Product=i.id):
        #     prod_off =  product_offer.objects.filter(Product=i.id)
        #     for poff in prod_off:
        #         if poff.status == True:
        #              cate_off = cat_offer.objects.filter(category=i.id)
        #              for coff in cate_off:
        #                 if coff.id == poff.id.id:
        #                     if coff.discount_amount < poff.offer_amount:
        #                         print("productname",poff.pid.series)
        #                         print("success yadhu")
        #                         amt = (poff.offer_amount*i.discount_amount)
        #                         i.price = i.discount_amoun-amt
        #                         i.save()
      
               
    
        context = {
            'category':category ,
            'products':products,
            'Banner':Banner,
           
            'category_offer1': category_offer1, 
            'product_offer1':product_offer1 
         }
       
        return render(request,'home.html',context)

def ProductDetail(request,id):
    
        try:
            category_offer = cat_offer.objects.all()
            single_product = product.objects.get(id=id)
            in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product = single_product).exists()
          
        except Exception as e:
            raise e
        context = {
            'single_product':single_product,
            'in_cart':in_cart,
            'category_offer':category_offer
        }
        return render(request,'product_detail.html',context)
    
def mens(request,id):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        if keyword:
            products = product.objects.order_by('created_date').filter(Q(productname__icontains=keyword))
            product_count = products.count()
            
            context = {
            'product':products,
             'product_count':products.count()
            }
            return render(request,'men.html',context)
    category = categories.objects.all()
    products = product.objects.filter(categories_id = id ,is_active=1)
    paginator = Paginator(products,3)
    product_count = products.count()
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
    'product': paged_products,
    'product_count':products.count(),
    'category': category
    }
    return render(request,'men.html',context)

# def search(request):
   
#     if 'keyword' in request.GET:
        
#         print("dsfsds",keyword)
#         if keyword:
       
            
            
#             print(products)

#     context = {
#         'product':products,
#         'product_count':products.count()
#     }
#     return render(request,'men.html',context)

def my_orders(request):
    orders = Order.objects.filter(user=request.user,is_ordered=False).order_by('-created_at')
    oreder1 = OrderProduct.objects.filter(user=request.user,ordered=True)
    print(orders)
    context = {
        'order1':oreder1,
        'orders':orders,
    }
    return render(request,'my_orders.html',context)
def cancel_order(request,order_id):

    order1 = Order.objects.get(id=order_id)
    print('cancel1',order1)
    order1.status='Cancelled'
    
    order1.save()
    return redirect('my_orders')

def return_order(request,id):
    print('add',id)
    order1 = Order.objects.get(id=id)
    print('order1',order1)
    order1.status = 'Returned'
    order1.save()
    return redirect('my_orders')




def my_profile(request):
    
    Amount = 0
    wallets = wallet.objects.filter(user= request.user)
    for sum in wallets:
        Amount += sum.Amount
    
    try:
        referal_code = referal.objects.filter(user=request.user)
    except:
        refer_code = referal()
        random_code = get_random_string(7, allowed_chars=string.ascii_uppercase + string.digits)
        refer_code.referal_code = referal_code
        refer_code.user = request.user
        refer_code.save()
    
    
    profile1 = address.objects.filter(user=request.user)
    print(profile1)
    refer1 = referal.objects.filter(user=request.user)
    context = {
       'profile1':profile1,
       'refer1':refer1,
       'wallets':wallets
   }
    return render(request,'my_profile.html',context)

def order_detail(request,order_id):
    order_details = OrderProduct.objects.filter(order__order_number = order_id)
    order = Order.objects.get(order_number=order_id)
    # subtotal = 0
    # for i in order_details:
    #     subtotal = i.price * i.quantity
    
    
    context = {
        'order_details':order_details,
        'order':order,
        # 'subtotal':subtotal
    }
    return render(request,'user_order_detail.html',context)

def profile_order_delete(request,id):
    del_order =  address.objects.get(id=id)
    del_order.delete()
    return render(request,'my_profile.html')
    
def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            messages.sucess(request,'Password reset email has been sent to your email')
            return redirect('login')
            
            
        else:
            messages.error(request,'Account doesnt exist')
            return redirect('forgotpassword')
    return render(request,'forgotpassword.html')
def resetpassword_validate(request):
    return HttpResponse('ok')

def edit_profile(request,id):
    obj1 = Account.objects.get(id=id)
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        
        obj1.first_name = first_name
        obj1.last_name = last_name
        obj1.email = email
        obj1.phone_number = phone_number
        
        obj1.save()
        
        return redirect(my_profile) 
    context = {
            'obj1':obj1
        }       
    return render(request,'edit_profile.html',context)

    
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        password = request.POST['password']
        confirm = request.POST.get('confirm_password')
        print(password)
        print(confirm)
        user = Account.objects.get(username__exact=request.user.username)
        print(user)
        if password == confirm:
            
            print("sfsdf")
            sucess = user.check_password(current_password)
            if sucess:
                user.set_password(password)
                user.save()
                auth.logout(request)
                messages.success(request,'Password Updated Sucessfully')
                return redirect(login)
            else:
                messages.error(request,'Please enter valid current password')
                return redirect(change_password)
        else:
            messages.error(request,'Password does not match')
            return redirect(change_password)
        
    return render(request,'change_password.html') 

def wallets(request):
    if request.method == 'POST':
        code = request.POST.get('r_code')  
        if code:
            ref = referal.objects.get(referal_code = code)
            wall = wallet()
            wall.user = ref.user
            wall.Amount = 50
            wall.save()
            
            
            wall = wallet()
            user_code =  referal.objects.get(user = request.user)
            wall.user = user_code.user
            wall.Amount = 20
            wall.save()
    return redirect(my_profile)

def export_to_pdf(request):
    y=[]
    z=[]
    a=product.objects.all()
    for i in a:
        b=i.id
        c=OrderProduct.objects.filter(product=b).count()
        y.append(i.product_name)
        z.append(c)
        e=i.price*c

    print(y,z)

    template_path = 'sales_pdf.html'
    context = {
        'brand_name':y,
        'order_count':z,
        'total_amount':e,
    }
    
    # csv file can also be generated using content_type='application/csv
    response = HttpResponse(content_type='application/pdf')
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
 
 
# def signup(request):
#    if request.method == 'POST':
#         username = request.POST['username']
#         firstname = request.POST['first_name']
#         lastname = request.POST['last_name']
#         email = request.POST['email']
#         password = request.POST.get('password')
#         password2 = request.POST.get('password2')
#         phonenumber = request.POST['phonenumber']
#         if(not firstname ):
#             messages.info(request, 'Firstname required ') 
#             return redirect('signup')
#         elif re.match("/^[a-z ,.'-]+$/i", firstname) != None:
#             messages.info(request, 'Firstname required characters ') 
#             return redirect('signup')
#         elif(not lastname):
#             messages.info(request, 'Lastname required')
#             return redirect('signup')
#         if len(email) > 12:
#             if re.match('\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', email) != None:
#                 messages.info(request, 'Valid email required')
#                 return redirect('signup')
#         elif len(email) < 12:
#             messages.info(request, 'Need atleast 6 in mail')
#             return redirect('signup')
        
        
#         if password == password2:
#             if customer.objects.filter(username=username).exists():
#                 messages.info(request, 'Username already exist') 
#                 return redirect('signup')
#             elif customer.objects.filter(email = email).exists():
#                 messages.info(request, 'Email already exist')
#                 return redirect('signup')
#             else:
#                 user = customer.objects.create(username = username, email = email, Firstname = firstname, Lastname = lastname,  password = password, Phonenumber = phonenumber,status = False)
#                 user.save()
                
#                 print('user created')
#                 return redirect('login')
            
#         else:
#             messages.info(request,"password not matching")
#             return redirect('signup')
#    else:
#         return render(request,'signup.html')
       




   
  #      try:
        #          print("Entering to try block")
        #          cart = Cart.objects.get(cart_id=_cart_id(request))
        #          is_cart_item_exists = CartItem.objects.filter(cart = cart).exists()
        #          print( is_cart_item_exists)
        #          if is_cart_item_exists:
        #              cart_item = CartItem.objects.filter(cart=cart)
        #              print(cart_item)
        #              for item in cart_item:
        #                  item.user = user
        #                  print(user)
        #                  item.save()
                
        #      except:
        #          print("Entering to exception block")
        #          pass
        #      block = customer.objects.get(username = username)
        #      if block.status == False:
        #         request.session['Session'] = '1'
        #         return render(request,'home.html',{'user':user})
        #      else:
        #          messages.info(request,'You are blocked')
        #          return render(request, 'login.html')
 
        
        
         