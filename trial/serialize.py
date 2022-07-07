from rest_framework import serializers
from trial.models import user,client ,items,Invoice,invoice_items,Billed_By,Billed_To,User_OTP
from django.contrib.auth.models import User

########################## Don't Use this since it's not encrypting the password ##################

class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields="__all__"

########################## Don't Use this since it's not encrypting the password ##################

class OtpSeraializer(serializers.ModelSerializer):
    class Meta:
        model= User_OTP
        fields="__all__"

class userSerializer(serializers.ModelSerializer):
    #### Used in putting some fields to necessary #######
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['user_phone'].required = True
    class Meta:
        model= user
        fields="__all__"


class clientSerializer(serializers.ModelSerializer):
    class Meta:
        model=client
        fields="__all__"

class itemsSerializer(serializers.ModelSerializer):
    class Meta:
        model=items
        fields="__all__"

class Billed_BySerializer(serializers.ModelSerializer):
    class Meta:
        model=Billed_By
        fields="__all__"

class Billed_ToSerializer(serializers.ModelSerializer):
    class Meta:
        model=Billed_To
        fields="__all__"

class invoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Invoice
        fields="__all__"
        #fields=["invoice_id","user_id","client_id","invoice_title","invoice_amount","invoice_status"]

class invoice_itemSerializer(serializers.ModelSerializer):
    class Meta:
        model=invoice_items
        fields="__all__"