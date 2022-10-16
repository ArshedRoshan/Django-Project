from ast import keyword
import datetime
from email.mime import image
from multiprocessing import context
from unicodedata import category
from django.shortcuts import render,redirect
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from user.models import Account
from django.contrib import messages
from adminpanel.models import *
from django.views.generic import ListView,CreateView,UpdateView,DetailView,DeleteView,View
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from .forms import BannerForm
from django.db.models import Q
from orders.models import Order,OrderProduct,Payment
from django.db.models.functions import ExtractMonth,ExtractYear
from django.db.models import Count
import calendar
from datetime import date
from django.http import HttpResponse
import xlwt
from django.template.loader import get_template
from xhtml2pdf import pisa 
from django.db.models import Sum
import csv
from django.views.decorators.cache import never_cache


# Create your views here.
def adminslogins(request):
   
    if 'adminSession' in request.session:
        return redirect('adminhome')
    if request.method == 'POST':
         username = request.POST['username']
         password = request.POST['password']

       
         log = adminlogin.objects.filter(username=username,password=password)
         if log:
            request.session['adminSession'] = '2'
            
            return render(request, 'admin.html',)
         else:
            messages.info(request, 'invalid credentials')
            return render(request, 'adminlogin.html')
    else:
        return render(request, 'adminlogin.html', )
@never_cache
def adminhome(request):
    if 'adminSession' in request.session:
        p=0
        a = []
        b = []
        graph = product.objects.all()
        for i in graph:
           z=i.id
           count = OrderProduct.objects.filter(Product=z).count()
           a.append(i.productname)
           b.append(count)
        pro = product.objects.all()
        for i in pro:
            p += i.stock
            print(p) 
        users = Account.objects.all().count()
        
        orders=Order.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id')).values('month','count')
        yearorders=Order.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(count=Count('id')).values('year','count')
        
        order1 = Order.objects.all()
        monthNumber=[]
        totalOrders=[]
        YearNumber=[]
        totaltyearorders=[]
        
        totals = order1.count
        print('total',totals)
        for d in orders:
            monthNumber.append(calendar.month_name[d['month']])
            print("dewdw",monthNumber)
            totalOrders.append(d['count'])
            print('fdafds',totalOrders)
        
        for d in yearorders:
            YearNumber.append([d['year']])
            print('year',YearNumber)
            totaltyearorders.append(d['count']) 
            print('totaltyearorders',totaltyearorders)
           
        context = {
            'labels':a,
            'data':b,
            'p':p,
            'users':users,
            'Order':orders,
            'MonthNumber':monthNumber,
           'TotalOrders':totalOrders,
           'totals':totals,
            'YearNumber': YearNumber,
            'totaltyearorders': totaltyearorders
        }
        
        return render(request,'admin.html',context)
    else:
        return render(request,'adminlogin.html')
    
@never_cache
def adminlogout(request):
    if 'adminSession' in request.session:
       del request.session['adminSession']
       return redirect('adminlogin')

def users(request):
        if 'adminSession' in request.session:
          value = Account.objects.all()
          print(value)
          return render(request,'users.html',{'value':value})
        else:
         return render(request,'adminlogin.html')
     
     
def blockuser(request,id):
    if 'adminSession' in request.session:
        user = Account.objects.get(id=id)
        if user.status is False:
            user.status = True
            user.save()
        else:
            user.status = False
            user.save()
        return redirect(users)
    else:
       return render(request,'adminlogin.html')
     


class CategoriesListView(ListView):
    model = categories
    template_name =  "category_list.html"
    
class CategoryCreate(SuccessMessageMixin,CreateView):
    model = categories
    success_message = "Category Added"
    fields = "__all__"
    template_name = "category_create.html"
    
class CategoryUpdate(SuccessMessageMixin,UpdateView):
     model = categories
     success_message = "Category Updated"
     fields = "__all__"
     template_name = "category_update.html"
     
class CategoryDelete(DeleteView):
    model = categories
    fields = "__all__"
    template_name = "category_delete.html"
    success_url =  reverse_lazy("category_list")
    


class SubCategoriesListView(ListView):
    model = Subcategories
    template_name =  "subcategory_list.html"
    
class SubCategoryCreate(SuccessMessageMixin,CreateView):
    model = Subcategories
 
    fields = "__all__"
    template_name = "subcategory_create.html"
    
class SubCategoryUpdate(SuccessMessageMixin,UpdateView):
    
     model = Subcategories
    
     fields = "__all__"
     template_name = "subcategory_update.html"
     
class SubCategoryDelete(LoginRequiredMixin,DeleteView):
    model = Subcategories
    fields = "__all__"
    template_name = "subcategory_delete.html"
    success_url =  reverse_lazy("subcategory_list")




def products(request):
    if 'adminSession' in request.session:
        # cat_data=categories.objects.all()
        product_data=product.objects.all()
        paginator = Paginator(product_data,3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        context = {
            'products_data':paged_products
        }
        return render(request, 'product.html',context)
    else:
        return render(request, 'adminlogin.html' )
    
    
# def search1(request):
#     if 'keyword' in request.GET:
#         keyword = request.GET['keyword']
#         if keyword:
#             product_data = product.objects.order_by('created_date').filter(Q(productname__icontains=keyword))
#             print(product_data)
#             print(keyword)
#         context = {
#             'products_data':product_data
#         }
#         return render(request, 'product.html',context)



def add_product(request):
    if 'adminSession' in request.session:
        cat_data = categories.objects.all()
        if request.method == 'POST':
            pro = product()
            pro.productname = request.POST.get('name')
            pro.price = request.POST.get('price')
            pro.dicscount_price = request.POST.get('dicscount_price')
            pro.stock = request.POST.get('stock')
            # pro.thumbnail = request.POST.get('thumbnail')
            a=request.POST.get("cats")
            pro.categories=categories.objects.get(id=a)
            pro.category_name = request.POST.get('category_name')
            pro.brand = request.POST.get('brand')
            pro.description = request.POST.get('description')
            
            if len(request.FILES) != 0:
                pro.image = request.FILES.get('image')
                pro.image2 = request.FILES.get('image2')
                pro.image3 = request.FILES.get('image3')
            pro.save()
            return redirect(products)
            # return render(request, 'owner/product.html', {"cat_data": cat_data,'products_data':product})
        else:
            return render(request, 'add_product.html',{"cat_data": cat_data})
   
    return render(request, 'adminlogin.html')

def ProductUpdate(request,id):
    
     if 'adminSession' in request.session:
         obj = product.objects.get(id=id)
         if request.method == 'POST':
            productname = request.POST.get('productname')
            print("hello",productname)
            price = request.POST.get('price')
            dicscount_price = request.POST.get('dicscount_price ')
            # thumbnail = request.POST.get('thumbnail')
            category_name = request.POST.get('category')
            brand = request.POST.get('brand')
            description = request.POST.get('description')
            stock = request.POST.get('stock')
            if len(request.FILES) != 0:
                obj.image = request.FILES.get('image')
             
            obj.productname = productname
            obj.price = price
            obj. dicscount_price  =  dicscount_price 
            obj.category_name = category_name 
            obj.brand = brand
            obj. description  = description
            obj.stock = stock
            # obj.image = image
           
            
            obj.save()
            return redirect('products_view')
         return render(request,'product_update.html',{'obj':obj})
     else:
         return render(request,'adminlogin.html')

def productdelete(request,id):
    if 'adminSession' in request.session:    
       
            pro = product.objects.get(id=id)
            pro.delete()
            return redirect('products_view')
    else:
        return render(request,'adminlogin.html')
    
def order_management(request):
    if 'adminSession' in request.session:  
        data = Order.objects.filter(is_ordered=False)
        data1 = OrderProduct.objects.filter(ordered=True)
        
        paginator = Paginator(data1,8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        context = {
            'data':data,
            'data1':paged_products
            
        }
        return render(request,'order_management.html',context)
    else:
        return render(request,'adminlogin.html')

def order_detail(request,order_id):
    if 'adminSession' in request.session:
        order_detail=OrderProduct.objects.filter(order__order_number=order_id)
        order=Order.objects.get(order_number = order_id)
        if request.method == 'POST':
            status =request.POST['Status']
            
            order.status=status
            order.save()
            
            
        context={
            'order_detail':order_detail,
            'order':order,

        }
        return render(request,'order_detail.html',context)
    else:
       return render(request,'adminlogin.html')

def banners(request):
    if 'adminSession' in request.session:
        Banner =  banner.objects.all()
        return render(request,'banner.html',{'banner_data':Banner})
    else:
        return render(request,'adminlogin.html')
    
def add_banner(request):
    if 'adminSession' in request.session:
        if request.method == "POST":
            
            content= request.POST['banner_title']
            content1 = request.POST['banner_title1']
            content2 = request.POST['banner_title2']
            banner_image  = request.FILES['banner_img']
            Banner = banner.objects.create(content=content, banner_image =  banner_image,content1=content1,content2=content2   )
            Banner.save()
            return redirect('banners')
        return render(request,'add_banner.html')
    else:
        return render(request,'adminlogin.html')
    
def delete_banner(request,banner_id):
    if 'adminSession' in request.session:
        del_data=banner.objects.get(id=banner_id)
        del_data.delete()
        return  redirect('banners')
    else:
        return render(request,'adminlogin.html')
    
def update_banner(request,id):
    if 'adminSession' in request.session:
        Banner =banner.objects.get(id=id)
        if request.method == "POST":
            Banner.content = request.POST['banner_title']
            Banner.content1 = request.POST['banner_title1']
            Banner.content2 = request.POST['banner_title2']
           
            if len(request.FILES) != 0:
                Banner.Banner = request.FILES['banner_img']
            Banner.save()
            return redirect('banners')
        return render(request, 'update_banner.html', {'banner_data': Banner})
    else:
        return render(request,'adminlogin.html')
    

def add_coupon(request):
    if 'adminSession' in request.session:
        if request.method == 'POST':
            offer = request.POST.get('discount')
            print('trtr',offer)
            coupon_code = request.POST.get('coupon_code') 
            valid_from = request.POST.get('valid_from')
            valid_to = request.POST.get('valid_to')
            max_limit = request.POST.get('max_limit')
            if int(offer) > 20:
                messages.warning(request,'Amount shoulbe less than 20%')
                return redirect('add_coupon')
            else:
                coupon = Coupon.objects.create(discount = offer, coupon_code = coupon_code,valid_from = valid_from,valid_to=valid_to,max_limit=max_limit)
                
                return redirect('coupon_list')
        else : 
            return render(request,'coupon_add.html')
    else:
        return render(request,'adminlogin.html')
        
def coupon_list(request):
    if 'adminSession' in request.session:
        coupon = Coupon.objects.all()
        
        cat_off = cat_offer.objects.all()
        
        offer1 = product_offer.objects.all()
        context = {
            'coupon':coupon,
            'cat_off':cat_off,
            'offer1':offer1
        }
        return render(request,'coupon_list.html',context)
    else:
        return render(request,'adminlogin.html')

def coupon_edit(request,id):
    if 'adminSession' in request.session:
        coupon_id = id
        if request.method == 'POST':
            if Coupon.objects.filter(id=coupon_id).exists():
                offr = Coupon.objects.filter(id=coupon_id)
                offer = request.POST['discount']
                coupon_code = request.POST['coupon_code'] 
                valid_from = request.POST.get('valid_from')
                valid_to = request.POST.get('valid_to')
                max_limit = request.POST.get('max_limit')
                
                offr.update(discount = offer, coupon_code = coupon_code,valid_from = valid_from,valid_to = valid_to,max_limit = max_limit)
                
                return redirect('coupon_list')
        else:
            coupon = Coupon.objects.get(id=coupon_id)
            context = { 
                'coupon_id' : coupon_id,
                'coupon': coupon
            }
            return render(request,'edit_coupon.html',context)
    else:
      return render(request,'adminlogin.html')
    
def coupon_disable(request,id):
    if 'adminSession' in request.session:
        coupon = Coupon.objects.get(id=id)
        coupon.delete()
            
        return redirect('coupon_list')
    else:
      return render(request,'adminlogin.html')
  
     
def add_cate_offer(request):
    if 'adminSession' in request.session:
        cat_data = categories.objects.all()
        print('haiii',cat_data)
        if request.method == 'POST':
            off = cat_offer()
            off.coupon_name = request.POST.get('coupon_name')
            print('coupon_name',off.coupon_name)
            off.valid_from = request.POST.get('valid_from')
            off.valid_to = request.POST.get('valid_to')
            off.discount_amount = request.POST.get('discount')
            k = request.POST.get('cats')
            off.category = categories.objects.get(id=k)
            if int(off.discount_amount) > 80:
                messages.warning(request,'Amount shoulbe less than 80%')
                return redirect('add_cate_offer')
            else:
                off.save()
                return redirect('cat_list')
        else : 
            return render(request,'add_cate_offer.html',{'cat_data':cat_data})
    else:
      return render(request,'adminlogin.html')
  
def cat_list(request):
    if 'adminSession' in request.session:
        cat_off = cat_offer.objects.all()
        
        context = {
            'cat_off':cat_off,
        }
        return render(request,'category_off.html',context)
    return render(request,'adminlogin.html')
    
    
    
def cat_offer_update(request,cat_id):
     if 'adminSession' in request.session:
        cat_id = id
        if request.method == 'POST':
            if cat_offer.objects.filter(id=cat_id).exists():
                offr = Coupon.objects.filter(id=cat_id)
                offer = request.POST['discount']
                coupon_name = request.POST['coupon_name'] 
                valid_from = request.POST.get('valid_from')
                valid_to = request.POST.get('valid_to')
                category = request.POST.get('category')
                
                offr.update(discount = offer, coupon_name = coupon_name,valid_from = valid_from,valid_to = valid_to)
                
                return redirect('cat_list')
        else:
            cat_of = cat_offer.objects.get(id=cat_id)
            context = { 
                'cat_id' : cat_id,
                'cat_of': cat_of
            }
            return render(request,'edit_coupon.html',context)
     else:
         return render(request,'adminlogin.html')
        
def cat_offer_delete(request,cat_id):
    if 'adminSession' in request.session:
        catt_of = cat_offer.objects.get(id=cat_id)
        print('dfd',catt_of)
        catt_of.delete()
        return redirect(cat_list)
    else:
         return render(request,'adminlogin.html')
     
def sales_report_date(request):
    data = OrderProduct.objects.all()
    if request.method == 'POST':
        if request.POST.get('month'):
            month = request.POST.get('month')
            print(month)
            data = OrderProduct.objects.filter(created_at__icontains=month)
            
            if data:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
                    for i in data:
                        sales = SalesReport()
                        sales.productName = i.Product.productname
                       
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales.html',context)
                else:
                    for i in data:
                        sales = SalesReport()
                        sales.productName = i.Product.productname
                       
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
                
        if request.POST.get('year'):
            year = request.POST.get('year')
            print(year)
            data = OrderProduct.objects.filter(created_at__icontains=year)
            
            if data:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
                    for i in data:
                        sales = SalesReport()
                        sales.productName = i.Product.productname
                       
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales.html',context)
                else:
                    for i in data:
                        sales = SalesReport()
                        sales.productName = i.Product.productname
                       
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
        
        
        
        
        
        
        if request.POST.get('date'):
            date = request.POST.get('date')
            print("0,",date)
            
            date_check = OrderProduct.objects.filter(created_at__icontains=date)
           
            if date_check:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
            
                    for i in date_check:
                        sales = SalesReport()
                        sales.productName = i.Product.productname
                      
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales.html',context)
                else:
                    for i in date_check:
                        sales = SalesReport()
                        sales.productName = i.Product.productname
                        
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
        if request.POST.get('date1'):
            date1 = request.POST.get('date1')
            date2 = request.POST.get('date2')
            data_range = OrderProduct.objects.filter(created_at__gte=date1,created_at__lte=date2)
            if data_range:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
            
                    for i in data_range:
                        sales = SalesReport()
                        sales.productName = i.Product.productname
                        
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales.html',context)
                else:
                    for i in data_range:
                        sales = SalesReport()
                        sales.productName = i.Product.productname
                        
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
    if data:
        if SalesReport.objects.all():
            SalesReport.objects.all().delete()
            for i in data:
                sales = SalesReport()
                sales.productName = i.Product.productname
              
                sales.date = i.created_at
                sales.quantity = i.quantity
                sales.productPrice = i.product_price
                sales.save()
            sales = SalesReport.objects.all()
            total = SalesReport.objects.all().aggregate(Sum('productPrice'))
            context = { 'sales':sales,'total':total['productPrice__sum']}
            return render(request,'sales.html',context)

        else:
            for i in data:
                sales = SalesReport()
                sales.productName = i.Product.productname
                
                sales.date = i.created_at
                sales.quantity = i.quantity
                sales.productPrice = i.product_price
                sales.save()
            sales = SalesReport.objects.all()
            total = SalesReport.objects.all().aggregate(Sum('productPrice'))
            context = { 'sales':sales,'total':total['productPrice__sum']}
            return render(request,'sales.html',context)
        
    else:
        messages.warning(request,"Nothing Found!!")
        
    
    
    return render(request,'sales.html')    


def export_to_excel(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['content-Disposition'] = 'attachment; filename="sales.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales Report') #this will generate a file named as sales Report

     # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Product Name','Category','Price','Quantity', ]

    for col_num in range(len(columns)):
        # at 0 row 0 column
        ws.write(row_num, col_num, columns[col_num], font_style)

    
    font_style = xlwt.XFStyle()
    total = 0

    rows = SalesReport.objects.values_list(
        'productName','categoryName', 'productPrice', 'quantity')
    for row in rows:
        total +=row[2]
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    row_num += 1
    col_num +=1
    ws.write(row_num,col_num,total,font_style)

    wb.save(response)

    return response

def export_to_pdf(request):
    prod = product.objects.all()
    order_count = []
    # for i in prod:
    #     count = SalesReport.objects.filter(product_id=i.id).count()
    #     order_count.append(count)
    #     total_sales = i.price*count
    sales = SalesReport.objects.all()
    total_sales = SalesReport.objects.all().aggregate(Sum('productPrice'))



    template_path = 'sales_pdf.html'
    context = {
        'brand_name':prod,
        'order_count':sales,
        'total_amount':total_sales['productPrice__sum'],
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

def monthly_export_to_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement; filename=SalesReport' +str(datetime.datetime.now())+'.csv'


    writer = csv.writer(response)
    writer.writerow(['Date ','Product Name ','Quantity  ','Amount'])

    reports = SalesReport.objects.all()

    for report in reports:
        writer.writerow([report.date , report.productName , report.quantity  , report.productPrice ])
    return response
     

def add_pro_offer(request):
     if 'adminSession' in request.session:
        pro_data = product.objects.all()
        print('products',pro_data)
        if request.method == 'POST':
            offer =  product_offer()
            offer.offer_name= request.POST.get('offer_name')
            offer.valid_from = request.POST.get('valid_from')
            offer.valid_to = request.POST.get('valid_to')
            print('coupon_name',offer.offer_name)
            offer.offer_amount = request.POST.get('offer_amount')
            k = request.POST.get('pro')
            offer.Product = product.objects.get(id=k)
            if int(offer.offer_amount) > 80:
                messages.warning(request,'Amount shoulbe less than 80%')
                return redirect('add_pro_offer')
            
            offer.save()
            return redirect('pro_list')
        else : 
            return render(request,'add_product_offer.html',{'pro_data':pro_data})
     else:
        return render(request,'adminlogin.html')
    
def pro_list(request):
    offer1 = product_offer.objects.all()
    context = {
        'offer1':offer1
    }
    return render(request,'pro_list.html',context)
    
    
def product_offer_delete(request,pro_id):
    if 'adminSession' in request.session:
        pro_of = product_offer.objects.filter(id=pro_id)
        print('dfd',pro_of)
        pro_of.delete()
        return redirect(pro_list)
    else:
       return render(request,'adminlogin.html')
    





# sales per day................
# def sales(request):
#     if 'adminSession' in request.session:
#         if 'date' in request.GET:
#             date = request.GET['date']
#             print("datesss",date)
#             Total = 0
#             if date:
#                 excel_products = sales_report.objects.all().delete()
#                 products =OrderProduct.objects.order_by('-created_at').filter(created_at__icontains=date)
#                 # print('products',products)
                
#                 for product in products:
#                     excel_products = sales_report()
#                     excel_products.date = product.created_at
#                     excel_products.product_name = product.Product.productname
#                     excel_products.quantity = product.quantity
#                     excel_products.amount = product.order.order_total
#                     Total += product.order.order_total
#                     excel_products.save()
                
#                 print('excel_product',excel_products)
#                 context = {
#                 'products':products,
#                 }
#                 return render(request,'sales.html',context)
#         return render(request,'sales.html')
#     else:
#          return render(request,'adminlogin.html')
# # sales per day excel download................

# def export_to_excel(request):
#     if 'adminSession' in request.session:
#         response = HttpResponse(content_type='application/ms-excel')
#         response['content-Disposition'] = 'attachment; filename="sales.xls"'
#         wb = xlwt.Workbook(encoding='utf-8')
#         # this will generate a file named as sales Report
#         ws = wb.add_sheet('Sales Report')

#         # Sheet header, first row
#         row_num = 0

#         font_style = xlwt.XFStyle()
#         font_style.font.bold = True

#         columns = ['Date','Product Name', 'Quantity', 'Amount', ]

#         for col_num in range(len(columns)):
#         # at 0 row 0 column
#             ws.write(row_num, col_num, columns[col_num], font_style)

#         font_style = xlwt.XFStyle()
#         total = 0
#         rows = sales_report.objects.all().values_list('date','product_name', 'quantity', 'amount')

#         print("row", rows)
#         for row in rows:
#             row_num += 1
#             for col_num in range(len(row)):
#                 ws.write(row_num, col_num, row[col_num], font_style)

#         wb.save(response)
#         return response
#     else:
#         return render(request,'adminlogin.html')

# def export_to_pdf(request):
#     if 'adminSession' in request.session:
#         total_sales = 0
#         report = sales_report.objects.all()
#         print('report',report)
#         sales = Order.objects.filter(status="Out of delivery").annotate(Count('id'))

#         for total_sale in report:
#             total_sales += total_sale.amount
#             print('total_sales',total_sales)

#         template_path = 'sales_pdf.html'
#         context = {
#             'report':report,
#             'total_amount':total_sales,
#         }
        
#         # csv file can also be generated using content_type='application/csv
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

#         template = get_template(template_path)
#         html = template.render(context)

#         # create a pdf
#         pisa_status = pisa.CreatePDF(
#             html, dest=response)
#         # if error then show some funny view
#         if pisa_status.err:
#             return HttpResponse('We had some errors <pre>' + html + '</pre>')

#         return response
#     else:
#         return render(request,'adminlogin.html')

# # sales per month.............................
# def monthly_sales(request):
#     if 'month_date' in request.GET:
#         month_date = request.GET['month_date']
#         Total = 0
#         if month_date:
#             excel_products = monthly_sales_report.objects.all().delete()
#             # months = OrderProduct.objects.annotate(month=ExtractMonth('created_at'))
#             months = OrderProduct.objects.filter(created_at__icontains = month_date)
           
#             for month in months:
#                 excel_products = monthly_sales_report()
#                 excel_products.date = month.created_at
#                 excel_products.product_name = month.Product.productname
#                 excel_products.quantity = month.quantity
#                 excel_products.amount = month.order.order_total
#                 Total += month.order.order_total
#                 excel_products.save()
#             context = {
#                 'month_products': months,
#                 'Total':Total
#             }
#             return render(request, 'sales.html', context)
#     return redirect(sales)

# def export_to_excel1(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['content-Disposition'] = 'attachment; filename="sales.xls"'
#     wb = xlwt.Workbook(encoding='utf-8')
#     # this will generate a file named as sales Report
#     ws = wb.add_sheet('Sales Report')

#     # Sheet header, first row
#     row_num = 0

#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True

#     columns = ['Date','Product Name', 'Quantity', 'Amount', ]

#     for col_num in range(len(columns)):
#     # at 0 row 0 column
#         ws.write(row_num, col_num, columns[col_num], font_style)

#     font_style = xlwt.XFStyle()
#     total = 0
#     rows = monthly_sales_report.objects.all().values_list('date','product_name', 'quantity', 'amount')
#     print("row", rows)
#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, row[col_num], font_style)

#     wb.save(response)
#     return response


# def export_to_pdf1(request):
#     Date = []
#     product_name= []
#     quantity =[]
#     amount=[]
#     rows = monthly_sales_report.objects.all()
#     for i in rows:
#         Date.append(i.date)
#         product_name.append(i.product_name)
#         quantity.append(i.quantity)
#         amount.append(i.amount)
    
#     template_path = 'sales_pdf.html'
#     context = {
#         'brand_name':Date,
#         'order_count':product_name,
#         'total_amount':quantity,
#         'amount':amount,
#     }
    
#     # csv file can also be generated using content_type='application/csv
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

#     template = get_template(template_path)
#     html = template.render(context)

#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#         html, dest=response)
#     # if error then show some funny view
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')

#     return response