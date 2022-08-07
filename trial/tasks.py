from celery import shared_task
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.core.mail import send_mass_mail,EmailMultiAlternatives 
from datetime import date
from django.conf.global_settings import DEFAULT_FROM_EMAIL
from .models import Invoice
from dateutil import parser
from django.core import mail
import requests
import os
import pdfkit
from .whatsapp import *

# @shared_task(bind=True)
# def test_func(self):
#     for i in range(10):
#         print(i)
#     return "Done"

def get_notification_email(data):
    email =[]
    email.append(EmailMultiAlternatives(
    data["subject"],
    data["body"],
    to=[data["email_to"]],
    bcc='',
    cc='',
    headers={'Message-ID': 'foo'},
    ))
    config = pdfkit.configuration(wkhtmltopdf = r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    options = {
    'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(data["email_pdf"], False, options,configuration = config)
    # with open('email_pdf.pdf', 'wb+') as f:
    #     f.write(pdf)
    email[-1].attach('testing.pdf',pdf ,'application/pdf')
    return email

@shared_task(bind=True)
def rem_email(self,data):
    invoice=Invoice.objects.filter(invoice_id=data["invoice_id"])
    due_date=invoice[0].Due_Date
    due_date_obj = parser.parse(due_date)
    remainder_date_obj=data['day']+'/'+data['month']+'/'+data['year']
    remainder_date_obj=parser.parse(remainder_date_obj)
    time_left=due_date_obj-remainder_date_obj
    time_left=time_left.total_seconds()/86400
    today = date.today()
    if str(today.year)==str(data['year']):
        if time_left>0:
            body=f"You are being reminded of your invoice due date attached below coming close which is in another {time_left} days i.e {due_date}.This is a automated mail.Don't Reply"
        elif time_left<0:
            body=f"You are being reminded of your invoice due date attached below which is over due of {time_left*(-1)} days i.e {due_date}.This is a automated mail.Don't Reply"
        else:
          body=f"You are being reminded of your invoice due date attached below which is due today i.e {due_date}.This is a automated mail.Don't Reply"
        # email=[]
        subject="Remainder Mail"
        # email.append((subject,body,DEFAULT_FROM_EMAIL,data["email_to"]))
        data['subject']=subject
        data['body']=body
        connection = mail.get_connection()   # Use default email connection
        messages = get_notification_email(data)  # accessing the get_notification_email function in utils.py file
        connection.send_messages(messages)
        # send_mass_mail(email,fail_silently=False)
        PeriodicTask.objects.filter(name__iexact=data["task_name"]).update(enabled=False)
        return True
    PeriodicTask.objects.filter(name__iexact=data["task_name"]).update(enabled=True)
    return False

@shared_task(bind=True)
def rem_whatsapp(self,data):
    invoice=Invoice.objects.filter(invoice_id=data["invoice_id"])
    due_date=invoice[0].Due_Date
    due_date_obj = parser.parse(due_date)
    remainder_date_obj=data['day']+'/'+data['month']+'/'+data['year']
    remainder_date_obj=parser.parse(remainder_date_obj)
    time_left=due_date_obj-remainder_date_obj
    time_left=time_left.total_seconds()/86400
    today = date.today()
    if str(today.year)==str(data['year']):
        if time_left>0:
            body=f"You are being reminded of your invoice due date attached above coming close which is in another {time_left} days i.e {due_date}.This is a automated mail.Don't Reply"
        elif time_left<0:
            body=f"You are being reminded of your invoice due date attached above which is over due of {time_left*(-1)} days i.e {due_date}.This is a automated mail.Don't Reply"
        else:
          body=f"You are being reminded of your invoice due date attached above which is due today i.e {due_date}.This is a automated mail.Don't Reply"
        config = pdfkit.configuration(wkhtmltopdf = r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
        options = {
        'encoding': "UTF-8",
        }
        pdf = pdfkit.from_string(data["whatsapp_pdf"], False, options,configuration = config)
        res=final_call(pdf,body)
        print(res)
        if res==1:
            PeriodicTask.objects.filter(name__iexact=data["task_name"]).update(enabled=False)
            return True
    PeriodicTask.objects.filter(name__iexact=data["task_name"]).update(enabled=True)
    return False