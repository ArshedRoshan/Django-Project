from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=50)
    status = models.BooleanField(max_length=10,default=False)
    status1 = models.BooleanField(max_length=10,null=True)
    
    

    # required
    date_joined     = models.DateTimeField(auto_now_add=True,null=True)
    last_login      = models.DateTimeField(auto_now_add=True,null=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=True)
    is_superadmin    = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

class Profile(models.Model):
    gender = (
        ('MEN', 'MEN'),
        ('FEMALE', 'FEMALE'),
        ('OTHERS', 'OTHERS')
    )
    STATUS = (
        ('HOME', 'HOME'),
        ('OFFICE', 'OFFICE'),
        ('OTHERS', 'OTHERS'),
    )
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile/',max_length=500,default='profile/avatar.png')
    first_name =  models.CharField(max_length=50 )
    last_name =  models.CharField(max_length=50, null = True)
  
    Phone_number = models.CharField(max_length=50) 
    gender = models.CharField(max_length=10, choices=gender, default='Male')
    house = models.CharField(max_length=50, null = True)
    town= models.CharField(max_length=50, null = True)
    locality= models.CharField(max_length=50, null = True)
    state = models.CharField(max_length=50, null = True)
    country = models.CharField(max_length=50, null = True)
    Address_type = models.CharField(max_length=10, choices=STATUS, default='HOME')

    
    zip = models.CharField(max_length=10 ,  blank=True, null=True)

    def __str__(self):
        return self.user.username

class wallet(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    Amount = models.IntegerField()


class referal(models.Model):
    referal_code = models.CharField(max_length=50)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)

class customer(models.Model):
    username = models.CharField(max_length=50)
    Firstname = models.CharField(max_length=50)
    Lastname = models.CharField(max_length=50)
    Phonenumber = models.CharField(max_length=15)
    email = models.CharField(max_length=100)
    password = models.CharField( max_length=50,null=True)
    status = models.BooleanField(max_length=10,null=True)
    status1 = models.BooleanField(max_length=10,null=True)
    

    
    
   
    
   
    
    
    
    
    
    
