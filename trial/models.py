from pydoc import cli
from pyexpat import model
from django.db import models
from pymysql import NULL
from django.contrib.auth.models import User
# Create your models here.


class User_OTP(models.Model):
    id=models.AutoField(primary_key=True)
    auth_id = models.OneToOneField(User, on_delete=models.CASCADE,null=False,blank=False)
    email_ver_OTP=models.CharField(max_length=6,blank=True,null=True)
    ver_OTP_time=models.DateTimeField(auto_now=True,blank=True,null=True)
    pass_change_otp=models.CharField(max_length=6,blank=True,null=True)
    pass_OTP_time=models.DateTimeField(auto_now=True,blank=True,null=True)
    email_verified=models.BooleanField(blank=True,null=True)

class user(models.Model):
    auth_id = models.OneToOneField(User,null= True, on_delete=models.SET_NULL)
    user_id = models.AutoField(primary_key=True)
    user_username = models.CharField(max_length=100, unique=True, null=False)
    user_email = models.EmailField(('email address'), unique=True, null=False)
    user_company = models.CharField(max_length=50,  default="None", null=True )
    user_address = models.CharField(max_length=150, default='None', null=True)
    user_phone = models.CharField(max_length=50, default="None", null=False,blank=False )


class client(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=100, unique=False)
    client_email = models.EmailField(('email address'), unique=True)
    client_company = models.CharField(max_length=50,  default="None", null=False )
    client_address = models.CharField(max_length=150, default='None', null=True)
    client_phone = models.CharField(max_length=50, default="None", null=False )
    user_id = models.ForeignKey(user,null= True, on_delete=models.SET_NULL)

#############Added item_GST_Rate,Quantity,Rate,Amount,CGST,SGST,Total###############
class items(models.Model):
    item_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(user,null= True, on_delete=models.SET_NULL)
    item_title = models.CharField(max_length=50, null=True)
    Rate=models.IntegerField(null=True)
    Quantity=models.IntegerField(null=True)
    item_GST_Rate=models.CharField(max_length=50, null=True)
    CGST=models.FloatField(null=True)
    SGST=models.FloatField(null=True)
    Total=models.FloatField(null=True)

################Added Billed To and Billed By database################

class Billed_By(models.Model):
    user_id = models.ForeignKey(user,null= True, on_delete=models.SET_NULL)
    Billed_By_id = models.AutoField(primary_key=True,default=None)
    Business_Name=models.CharField(max_length=50,  default="None", null=False )
    Street=models.CharField(max_length=150,  default="None", null=True )
    City=models.CharField(max_length=150,  default="None", null=True )
    Country=models.CharField(max_length=150,  default="None", null=True )
    Pincode=models.CharField(max_length=150,  default="None", null=True )
    Address=models.CharField(max_length=150,  default="None", null=True )
    Email=models.CharField(max_length=50,  default="None", null=False )
    Phone=models.CharField(max_length=50,  default="None", null=False )
    Business_GSTIN=models.IntegerField(null=True)
    Business_PAN_Number=models.CharField(max_length=50,  default="None", null=True )
    VAT_Registration_Number=models.CharField(max_length=50,  default="None", null=True )

class Billed_To(models.Model):
    user_id = models.ForeignKey(user,null= True, on_delete=models.SET_NULL)
    Billed_To_id = models.AutoField(primary_key=True,default=None)
    Business_Name=models.CharField(max_length=50,  default="None", null=False )
    Street=models.CharField(max_length=150,  default="None", null=True )
    City=models.CharField(max_length=150,  default="None", null=True )
    Country=models.CharField(max_length=150,  default="None", null=True )
    Pincode=models.CharField(max_length=150,  default="None", null=True )
    Address=models.CharField(max_length=150,  default="None", null=True )
    Email=models.CharField(max_length=50,  default="None", null=False )
    Phone=models.CharField(max_length=50,  default="None", null=False )
    Business_GSTIN=models.IntegerField(null=True)
    Business_PAN_Number=models.CharField(max_length=50,  default="None", null=True )
    VAT_Registration_Number=models.CharField(max_length=50,  default="None", null=True )
    Unique_Key=models.CharField(max_length=50,  default="None", null=True )

################Added invoice_subtitle,Invoice_Date,Due_Date###########
################Added Invoice_Billed_To,Inovice_Billed_By,Invoice_tax,Invoice_currency###########
################Added Invoice_amount,

class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    user_id=models.ForeignKey(user,null=True, on_delete=models.SET_NULL)
    #client_id=models.ForeignKey(client,null=True, on_delete=models.SET_NULL)
    invoice_title=models.CharField(max_length=1000)
    invoice_subtitle=models.CharField(max_length=1000)
    Invoice_Date=models.CharField(max_length=50, default="None", null=False)
    Due_Date=models.CharField(max_length=50, default="None", null=False)
    Invoice_Billed_By=models.ForeignKey(Billed_By,null=True, on_delete=models.SET_NULL)
    Invoice_Billed_To=models.ForeignKey(Billed_To,null=True, on_delete=models.SET_NULL)
    Invoice_tax=models.CharField(max_length=50, default="None", null=False)
    Invoice_currency=models.CharField(max_length=50,  default="None", null=False )
    Invoiceitems=models.ManyToManyField(items)
    # Invoiceitems=models.ForeignKey(items,null=True, on_delete=models.SET_NULL)
    Invoice_subtot=models.FloatField(null=True,default= 0)
    Invoice_ship=models.FloatField(null=True,default= 0)
    Invoice_disc=models.FloatField(null=True,default= 0)
    Invoice_Total=models.FloatField(null=True,default= 0)
    #Invoice_amount=models.FloatField(null=True,default= 0)
    Invoice_status = models.IntegerField(default= 0 ,null=True)
    Amount_inwords=models.CharField(max_length=1000, default="None", null=False)

class invoice_items(models.Model):
    invoice_id = models.ForeignKey(Invoice,null=True, on_delete=models.SET_NULL)
    item_id = models.ForeignKey(items,null=True, on_delete=models.SET_NULL)
    item_quantity = models.IntegerField(null=True)