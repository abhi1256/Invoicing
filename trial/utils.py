
from django.core.mail import EmailMultiAlternatives
import requests
import os
import random as r
from django.core.mail import send_mail
from django.conf.global_settings import DEFAULT_FROM_EMAIL
 
def invoice_func(Data):
    Invoice_list={
        "user_id": Data["user_id"],
        # "client_id": Data["client_id"],
        "invoice_title": Data["Invoice_name"],
        "invoice_subtitle": Data["Invoice_Sub_Title"],
        "Invoice_Date": Data["Invoice_Date"],
        "Due_Date": Data["Due_Date"],
        "Invoice_Billed_By": Data["bil_by_id"],
        "Invoice_Billed_To": Data["bil_to_id"],
        "Invoice_tax": Data["Choose_Taxation"],
        "Invoice_currency": Data["Currency"],
        "Invoiceitems": Data["items"],
        "Invoice_amount": Data["Total_sum"],
        "Invoice_status": Data["status"],
    }
    return Invoice_list

def inv_up_func(Data):
    Invoice_list={
        "invoice_title": Data["Invoice_name"],
        "invoice_subtitle": Data["Invoice_Sub_Title"],
        "Invoice_Date": Data["Invoice_Date"],
        "Due_Date": Data["Due_Date"],
        "Invoice_tax": Data["Choose_Taxation"],
        "Invoice_currency": Data["Currency"],
        "Invoice_amount": Data["Total_sum"],
        "Invoice_status": Data["status"],
    }
    return Invoice_list


def Billed_By_func(Data):
    billed_by_list={
        "Business_Name":Data["Billed_By"]["Business_Name"],
        "Address": Data["Billed_By"]["Address"],
        "Email": Data["Billed_By"]["Email"],
        "Phone": Data["Billed_By"]["Phone"],
        "Business_GSTIN": Data["Billed_By"]["Business_GSTIN"],
        "Business_PAN_Number": Data["Billed_By"]["Business_PAN_Number"],
        "VAT_Registration_Number": Data["Billed_By"]["VAT_Registration_Number"],
        "user_id":Data["user_id"]
    }
    return (billed_by_list)
def Billed_To_func(Data):
    billed_to_list={
        "Business_Name":Data["Billed_To"]["Business_Name"],
        "Address": Data["Billed_To"]["Address"],
        "Email": Data["Billed_To"]["Email"],
        "Phone": Data["Billed_To"]["Phone"],
        "Business_GSTIN": Data["Billed_To"]["Business_GSTIN"],
        "Business_PAN_Number": Data["Billed_To"]["Business_PAN_Number"],
        "VAT_Registration_Number": Data["Billed_To"]["VAT_Registration_Number"],
        "Unique_Key":Data["Billed_To"]["Unique_Key"],
        "user_id":Data["user_id"]
    }
    return (billed_to_list)

def item_func(Data):
    item_list=[]
    for j in Data['Item']:   ##### iterating over the items section in the invoice ###########
        item={
            "item_id":1,
            "user_id":Data['user_id'],
            "item_title":j['item_name'],
            "item_GST_Rate":j['GST Rate'],
            "Quantity":j['Quantity'],
            "Rate":j['Rate'],
            "Amount":j['Amount'],
            "CGST":j['CGST'],
            "SGST":j['SGST'],
            "Total":j['Total']
        }
        item_list.append(item)
    return item_list

def item_up_func(Data):
    item_list={
        "item_title":Data['item_name'],
        "item_GST_Rate":Data['GST Rate'],
        "Quantity":Data['Quantity'],
        "Rate":Data['Rate'],
        "Amount":Data['Amount'],
        "CGST":Data['CGST'],
        "SGST":Data['SGST'],
        "Total":Data['Total']
    }
    return item_list


def invoice_items_func(Data):
    invoice_items_list=[
        'invoice_id',
        'item_id',
        'item_quantity'
    ]
    return invoice_items_list

def get_notification_email(data):
    email =[]
    for j in data["emails"]:          ################# iterating over all the to emails in the emails section ##########
        email.append(EmailMultiAlternatives(
        j["email_subject"],
        j["email_body"],
        to=j["email_to"],
        bcc=j["email_bcc"],
        cc=j["email_cc"],
        headers={'Message-ID': 'foo'},
        ))
        r=False
        try:
            r = requests.get(j["email_pdf"], allow_redirects=True)
        except:
            pass
        if r:
            attachment = open('test.pdf', 'wb').write(r.content)
            attachment = open('test.pdf', 'rb')
            email[-1].attach('testing.pdf',attachment.read() ,'application/pdf')
            attachment.close()
            os.remove('test.pdf')
    return email



########################## function for otp generation and sending it via a mail #############################
def otpgen(email):
    otp=""
    for i in range(6):
        otp+=str(r.randint(1,9))
    to_email=email
    subject=f'OTP:{otp}'
    body=f"This is a automated MSG.Pls don't reply.This is your OTP:{otp}"
    print(body,to_email)
    send_mail(subject,body,from_email=DEFAULT_FROM_EMAIL,recipient_list=[to_email])
    return otp



def Dict_Key_Changer(data,name,suffix,prefix):
    keys=list(data.keys())
    for i in range(len(keys)):
        if suffix==1:
            new_key=name+keys[i]
        elif prefix==1:
            new_key=keys[i]+name
        else:
            new_key=name
        data[new_key] = data.pop(keys[i])
    return data