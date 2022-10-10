from django.db import models

# Create your models here.
from turtle import onkey
from django.db import models
from adminpanel . models import product
from user . models import Account

# Create your models here.
class Wish(models.Model):
    wish_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self):
       return self.wish_id

    
class WishItem(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,default=True)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    wish = models.ForeignKey(Wish,on_delete=models.CASCADE,default=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return str(self.product)
