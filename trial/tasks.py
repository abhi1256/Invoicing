from celery import shared_task
from django.core.mail import send_mass_mail 
from datetime import date
from django.conf.global_settings import DEFAULT_FROM_EMAIL
# @shared_task(bind=True)
# def test_func(self):
#     for i in range(10):
#         print(i)
#     return "Done"

@shared_task(bind=True)
def rem_email(self,data):
    today = date.today()
    #print(data)
    if str(today.year)==str(data['year']):
        email=[]
        #print(data,'hi')
        subject="Remainder Mail"
        body=f"This is to inform u that u have added a remainder to remaind you on {data['day']}-{data['month']}-{data['year']} regarding the job application.This is a automated mail.Don't Reply"
        email.append((subject,body,DEFAULT_FROM_EMAIL,data["email_to"]))
        #print(email)
        send_mass_mail(email,fail_silently=False)
        return True