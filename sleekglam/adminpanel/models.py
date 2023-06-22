from distutils.command.upload import upload
from email.policy import default
from math import trunc
from pickle import TRUE
from unittest.util import _MAX_LENGTH
from django.db import models
from django .dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

from user.models import Account
# Create your models here.

class adminlogin(models.Model):
   username = models.CharField( max_length=50)
   password = models.CharField(max_length=25)

class categories(models.Model):
   # id = models.AutoField(primary_key=True)
   title = models.CharField(max_length=255)
   slug = models.SlugField(max_length=255)
   thumbnail = models.ImageField(upload_to = 'static')
   description = models.TextField()
   is_active = models.IntegerField(default=1)
   status = models.BooleanField(default=False,help_text="0=default, 1=Trending")
   created_at = models.DateTimeField(auto_now_add=True)
   
   def get_absolute_url(self):
       return reverse("category_list")
   def __str__(self) :
       return self.title
   
   
class Subcategories(models.Model):
   # id = models.AutoField(primary_key=True)
   categories_id = models.ForeignKey(categories,on_delete=models.CASCADE,null=True)
   title = models.SlugField(max_length=255)
   url_slug = models.CharField(max_length=255)
   thumbnail = models.ImageField(upload_to = 'static')
   description = models.TextField()
   created_at = models.DateTimeField(auto_now_add=True)
   is_active = models.IntegerField(default=1)
   
   def get_absolute_url(self):
       return reverse("subcategory_list")
   
class product(models.Model):
   # id = models.AutoField(primary_key=TRUE)
   slug = models.SlugField(max_length=255,default=True)
   # subcategories_id=models.ForeignKey(Subcategories,on_delete=models.CASCADE,default=True)
   categories = models.ForeignKey(categories,on_delete=models.CASCADE,null=True)
   productname = models.CharField(max_length=200)
   brand = models.CharField(max_length=255,null=True)
   price = models.IntegerField()
   dicscount_price =  models.CharField(max_length=255,null=True)
   description = models.TextField()
   image = models.FileField(default=True,upload_to='static')
   is_active = models.IntegerField(default=1)
   category_name = models.CharField(max_length=250,null=True)
   image2 = models.FileField(default=True,upload_to='static')
   image3 = models.FileField(default=True,upload_to='static')
   stock = models.IntegerField(null=True)
   created_date = models.DateTimeField(auto_now_add=True,null=True)
   modified_date = models.DateTimeField(auto_now_add=True,null=True)
   product_offer1 = models.IntegerField(null = True)
   
   def get_url(self):
      return reverse('product_detail',args=[self.category.slug,self.slug])
   def __str__(self):
      return self.productname
   


variation_category_choice = (
('size','size'),
)   
class Variation(models.Model):
   product = models.ForeignKey(product,on_delete=models.CASCADE)
   variation_category = models.CharField(max_length=100,choices=variation_category_choice)
   variation_value =  models.CharField(max_length=100)
   is_active = models.BooleanField(default=TRUE)
   created_date = models.DateField(auto_now=TRUE)
   
   def __str__(self):
      return self.product
   
class ProductMedia(models.Model):
   #  id = models.AutoField(primary_key=TRUE)
    product_id = models.ForeignKey(product,on_delete=models.CASCADE)
    media_type_choice = ((1,"image"),(2,"video"))
    media_type  = models.CharField(max_length=255)
    media_content = models.FileField()
    is_active = models.IntegerField(default=1)

class banner(models.Model):
    banner_image =models.ImageField( upload_to='static', height_field=None, width_field=None, max_length=None,blank=True)
    content = models.CharField(max_length=250,null=True)
    content1 = models.CharField(max_length=40,null=True)
    content2 = models.CharField(max_length=30,null=True)
    
class Coupon(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    coupon_code = models.CharField(max_length=30,unique=True)
    valid_from = models.DateTimeField( null = True)
    valid_to = models.DateTimeField( null = True )
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    max_limit = models.CharField(max_length=20,null=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.coupon_code

class cat_offer(models.Model):
   coupon_name = models.CharField(max_length=50)
   category = models.ForeignKey(categories,on_delete=models.CASCADE,null=True)
   valid_from = models.DateField(null=True)
   valid_to = models.DateField( null=True)
   discount_amount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
   active = models.BooleanField(default=True)
   
   def __str__(self):
        return self.coupon_name

class sales_report(models.Model):
    date = models.DateField(null=True)
    product_name = models.CharField(null=True,max_length=100)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)


class monthly_sales_report(models.Model):
    date = models.DateField(null=True)
    product_name = models.CharField(null=True, max_length=100)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)


class SalesReport(models.Model):
    productName = models.CharField(max_length=100)
    categoryName = models.CharField(max_length=100)
    date = models.DateField()
    quantity = models.IntegerField()
    productPrice = models.FloatField()

class product_offer(models.Model):
    offer_name = models.CharField(max_length= 100,null = True)
    Product = models.ForeignKey(product,on_delete=models.CASCADE,null=True)
    offer_amount = models.IntegerField()
    status = models.BooleanField(default=True)
    valid_from = models.DateField(null=True)
    valid_to = models.DateField( null=True)