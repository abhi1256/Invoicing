import re
from urllib import response
from wsgiref import headers
from django.shortcuts import redirect, render, HttpResponse
from flask import url_for
from grpc import Status
from matplotlib.style import use
from numpy import inexact
import requests
from sklearn import exceptions
from .forms import InvoiceForm
from fpdf import FPDF
import http.client
import json
import base64
from io import BytesIO
from django.http import HttpResponse,JsonResponse,FileResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .whatsapp import *
from .pdf import *
from .utils import *
from .Invoice_Parser import *  
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import user,client,Invoice,items,Billed_By,Billed_To,User_OTP
from .serialize import OtpSeraializer, userSerializer,clientSerializer,itemsSerializer,invoiceSerializer,Billed_BySerializer,Billed_ToSerializer,User_OTP,AuthSerializer
################## Django mail related libraries Added by Abhiram ###################
from django.http import HttpResponse
from django.core import mail
################## Django celery related libraries Added by Abhiram ###################
from .tasks import * 
from django_celery_beat.models import PeriodicTask, CrontabSchedule
################## Django Authentication Libs Added by Abhiram ########################
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, tzinfo
from django.utils import timezone
import pytz
from itertools import chain
from django.db.models import Q
from django.template.loader import render_to_string
from django.template import loader
import pdfkit
import PyPDF2
from requests_toolbelt.multipart.encoder import MultipartEncoder

# from weasyprint import HTML


class usersList(LoginRequiredMixin,APIView):
    login_url='/login/'
    def get(self,request):
        user1=user.objects.all() # If this api needs to be safely authenticated uncomment below line.
        #user2=[u for u in user1 if u.user_email==request.user.email] 
        serializer=userSerializer(user1,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=userSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class userDetails(LoginRequiredMixin,APIView):
    login_url='/login/'
    def get(self,request):
        try:
            user1=user.objects.get(user_email__iexact=request.user.email)
        except:
            return HttpResponse(status=404)
        serializer=userSerializer(user1)
        return Response(serializer.data)
    
    def delete(self,request):
        try:
            user1=user.objects.get(user_id=request.data["user_id"])
        except:
            return HttpResponse(status=404)
        user1.delete()
        return HttpResponse("Item Deleted!",status=status.HTTP_204_NO_CONTENT)



################################## Changed Items API to better fit for my data json ##################################

class userItems(LoginRequiredMixin,APIView):

    login_url='/login/'
    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, *args, **kwargs):
        # print(self.request.POST,self.request)
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(userItems, self).dispatch(*args, **kwargs)

    def post(self,request):
        user1=user.objects.get(user_email__iexact=request.user.email)
        item_data=item_func(request.data)
        # print('item',item_data)
        serializer=itemsSerializer(data=item_data,many=True)
        # print('serializer.is_valid()',serializer.is_valid())
        if serializer.is_valid():
            for i in range(len(item_data)):
                serializer.validated_data[i]['user_id']=user1
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def get(self,request):
        
        user1=user.objects.get(user_email__iexact=request.user.email)
        allitem=items.objects.filter(user_id=user1)
        serializer=itemsSerializer(allitem,many=True)
        return Response(serializer.data)

    def delete(self,request):
        try:
            user1=user.objects.get(user_email__iexact=request.user.email)
            item1=items.objects.get(item_id=request.data["item_id"])
            if user1.user_id!=item1.user_id:
                return HttpResponse("Not authorized",status=404)
        except:
            return HttpResponse(status=404)
        item1.delete()
        return HttpResponse("Item Deleted!",status=status.HTTP_204_NO_CONTENT)

    def put(self,request):
        if type(request.data["item_ids"])==list:
            i=0
            if len(request.data["item_ids"])<=len(request.data["Item"]):
                for item_id in request.data["item_ids"]:
                    try:
                        allitem=items.objects.filter(item_id=item_id)
                        user1=user.objects.get(user_id=request.data['user_id'])
                    except:
                        return HttpResponse("Either Item is not found or user is not there",status=404)
                    if request.user.email==user1.user_email:
                        item_li=item_up_func(request.data["Item"][i])
                        allitem.update(**item_li)
                        i+=1
                data={"Item":[],"user_id":request.data["user_id"]}
                for j in range(i,len(request.data["Item"])):
                    data['Item'].append(request.data["Item"][j])
                if len(data['Item'])!=0:
                    item_data=item_func(data)
                    serializer=itemsSerializer(data=item_data,many=True)
                    if serializer.is_valid():
                        for i in range(len(item_data)):
                            serializer.validated_data[i]['user_id']=user1
                        serializer.save()
                        return Response(serializer.data,status=status.HTTP_206_PARTIAL_CONTENT)
                else:
                    return HttpResponse("Item Updated!",status=status.HTTP_200_OK)
                return HttpResponse("Item Couldn't Update!",status=status.HTTP_400_BAD_REQUEST)
            elif len(request.data["item_ids"])>len(request.data["Item"]):
                for i in range(len(request.data["Item"])):
                    try:
                        allitem=items.objects.filter(item_id=request.data["item_ids"][i])
                        user1=user.objects.get(user_id=request.data['user_id'])
                    except:
                        return HttpResponse("Either Item is not found or user is not there",status=404)
                    if request.user.email==user1.user_email:
                        item_li=item_up_func(request.data["Item"][i])
                        allitem.update(**item_li)
                        # i+=1
                for j in range(len(request.data["Item"]),len(request.data["item_ids"])):
                    del_item=items.objects.get(item_id=request.data["item_ids"][j])
                    del_item.delete()
                return HttpResponse("Item Updated!",status=status.HTTP_200_OK)
        return HttpResponse("Item Updated!",status=status.HTTP_200_OK)

################# Caution this below api get is not protected i.e any user can use this to see all items of others ###########
################# for the protected one u can use userItems get api #################################

class itemsList(LoginRequiredMixin,APIView):
    login_url='/login/'
    def get(self,request):
        item1=items.objects.all()
        serializer=itemsSerializer(item1,many=True)
        return Response(serializer.data)

class userClients(LoginRequiredMixin,APIView):
    login_url='/login/'
    def post(self,request):
        user1=user.objects.get(user_email__iexact=request.user.email)
        serializer=clientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user_id']=user1
            serializer.save()

            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        user1=user.objects.get(user_email__iexact=request.user.email)
        try:
            allclients=client.objects.filter(user_id=user1)
        except exceptions as e:
            return HttpResponse("You are not authorized!!",status=status.HTTP_401_UNAUTHORIZED)
        serializer=clientSerializer(allclients,many=True)
        return Response(serializer.data)
    

    def delete(self,request):
        try:
            client1=client.objects.get(client_id=request.data["client_id"])
            user1=user.objects.get(user_email__iexact=request.user.email)
        except:
            return HttpResponse(status=404)
        if client.user_id==user1.user_id:
            client1.delete()
        else:
            return HttpResponse("You are not authorized!!",status=status.HTTP_401_UNAUTHORIZED)
        return HttpResponse("Client Deleted!",status=status.HTTP_204_NO_CONTENT)

############################# Billed_BY API added by Abhiram #############################################

class billed_by(LoginRequiredMixin,APIView):
    login_url='/login/'
    http_method_names = ['get', 'post', 'put', 'delete']


    def dispatch(self, *args, **kwargs):
        # print(self.request.POST,self.request)
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(billed_by, self).dispatch(*args, **kwargs)


    def get(self,request):
        user1=user.objects.get(user_email__iexact=request.user.email)
        invoices=Invoice.objects.filter(user_id=user1.user_id)
        ids=[]
        for i in invoices.values("Invoice_Billed_By_id"):
            ids.append(i["Invoice_Billed_By_id"])
        billed_by1=Billed_By.objects.filter(Billed_By_id__in=ids)
        serializer=Billed_BySerializer(billed_by1,many=True)

        return Response(serializer.data)
    
    def post(self,request):
        # print(request.data,'bill_by')
        bi_data=Billed_By_func(request.data)
        serializer=Billed_BySerializer(data=bi_data)
        # print('ser',serializer)
        # print("ser_ver",serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data,status=status.HTTP_201_CREATED)#,safe=False)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)##,safe=False)
    
    # def delete(self,request):
    #     try:
    #         Billed_by=Billed_By.objects.get(Billed_By_id=request.data["Billed_By_id"])
    #     except:
    #         return HttpResponse(status=404)
    #     Billed_by.delete()
    #     return HttpResponse("Billed_To Deleted!",status=status.HTTP_204_NO_CONTENT)

    def put(self,request):
        # print(request.data,'hi bil_by')
        try:
            bil_by=Billed_By.objects.filter(Billed_By_id=request.data["bil_by_id"])
            user1=user.objects.get(user_id=request.data["user_id"])
        except:
            return HttpResponse("Either Item is not found or user is not there",status=404)
        if request.user.email==user1.user_email:
            bil_by_li=Billed_By_func(request.data)
            bil_by.update(**bil_by_li)
        return HttpResponse("Item Updated!",status=status.HTTP_200_OK)
############################# Billed_TO API added by Abhiram #############################################

class billed_to(LoginRequiredMixin,APIView):
    login_url='/login/'
    http_method_names = ['get', 'post', 'put', 'delete']


    def dispatch(self, *args, **kwargs):
        # print(self.request.POST,self.request)
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(billed_to, self).dispatch(*args, **kwargs)


    def get(self,request):
        user1=user.objects.get(user_email__iexact=request.user.email)
        invoices=Invoice.objects.filter(user_id=user1.user_id)
        ids=[]
        for i in invoices.values("Invoice_Billed_To_id"):
            ids.append(i["Invoice_Billed_To_id"])
        billed_to1=Billed_To.objects.filter(Billed_To_id__in=ids)
        serializer=Billed_ToSerializer(billed_to1,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        bi_data=Billed_To_func(request.data)
        serializer=Billed_ToSerializer(data=bi_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        try:
            Billed_to=Billed_To.objects.get(Billed_To_id=request.data["Billed_To_id"])
        except:
            return HttpResponse(status=404)
        Billed_to.delete()
        return HttpResponse("Billed_To Deleted!",status=status.HTTP_204_NO_CONTENT)

    def put(self,request):
        try:
            bil_to=Billed_To.objects.filter(Billed_To_id=request.data["bil_to_id"])
            user1=user.objects.get(user_id=request.data["user_id"])
        except:
            return HttpResponse("Either Item is not found or user is not there",status=404)
        if request.user.email==user1.user_email:
            bil_to_li=Billed_To_func(request.data)
            bil_to.update(**bil_to_li)
        return HttpResponse("Item Updated!",status=status.HTTP_200_OK)

class invoiceList(LoginRequiredMixin,APIView):
    login_url='/login/'
    def get(self,request):
        invoice1=Invoice.objects.all()
        serializer=invoiceSerializer(invoice1,many=True)
        return Response(serializer.data)

############################# Invoice API added by Abhiram #############################################

class User_invoiceList(LoginRequiredMixin,APIView):
    login_url='/login/'
    def get(self,request):
        json_data=request.data
        invoice1=Invoice.objects.filter(invoice_id=json_data["invoice_id"])
        user1=user.objects.get(user_id=invoice1.values("user_id")[0]["user_id"])
        if user1.user_email==request.user.email:
            serializer=invoiceSerializer(invoice1,many=True)
            for i in range(len(serializer.data)):
                user1=user.objects.filter(user_id=serializer.data[i]['user_id'])
                # client1=client.objects.filter(client_id=serializer.data[i]['client_id'])
                BB1=Billed_By.objects.filter(Billed_By_id=serializer.data[i]['Invoice_Billed_By'])
                BT1=Billed_To.objects.filter(Billed_To_id=serializer.data[i]['Invoice_Billed_To'])
                US=userSerializer(user1,many=True)
                # CS=clientSerializer(client1,many=True)
                BBS=Billed_BySerializer(BB1,many=True)
                BTS=Billed_BySerializer(BT1,many=True)
                serializer.data[i]['Invoice_Billed_By']=BBS.data[0]
                serializer.data[i]['Invoice_Billed_To']=BTS.data[0]
                serializer.data[i]['user']=US.data[0]["user_username"]
                # serializer.data[i]['client']=CS.data[0]["client_name"]
                serializer.data[i]['Invoice_Billed_By'].pop('user_id')
                serializer.data[i]['Invoice_Billed_To'].pop('user_id')
                serializer.data[i].pop('user_id')
                # serializer.data[i].pop('client_id')
                for j in range(len(serializer.data[0]['Invoiceitems'])):
                    item1=items.objects.filter(item_id=serializer.data[i]['Invoiceitems'][j])
                    serializer1=itemsSerializer(item1,many=True)
                    serializer.data[i]['Invoiceitems'][j]=serializer1.data[0]
                    serializer.data[i]['Invoiceitems'][j].pop('user_id')
            return Response(serializer.data,status=status.HTTP_200_OK)
        return HttpResponse("User Not Verified",status=status.HTTP_401_UNAUTHORIZED)
        
############################# Invoice API added by Abhiram #############################################    

class userInvoices(LoginRequiredMixin,APIView):
    login_url='/login/'
    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, *args, **kwargs):
        # print(self.request.POST,self.request)
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(userInvoices, self).dispatch(*args, **kwargs)

    def post(self,request):
        in_data=invoice_func(request.data)
        serializer=invoiceSerializer(data=in_data)
        serializer.is_valid()
        #print(serializer.errors)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

    def get(self,request):
        # print(request.data)
        auth=User.objects.get(email__iexact=request.user.email)
        user_id=user.objects.get(auth_id=auth)
        #pk=request.data["user_id"]
        #ck=request.data["client_id"]
        #print(pk,ck)
        if user_id.user_email==request.user.email:
            invoice1=Invoice.objects.filter(user_id=user_id)#,client_id=ck)
            #print(invoice1)
            serializer=invoiceSerializer(invoice1,many=True)
            for i in range(len(serializer.data)):
                user1=user.objects.filter(user_id=serializer.data[i]['user_id'])
                #client1=client.objects.filter(client_id=serializer.data[i]['client_id'])
                BB1=Billed_By.objects.filter(Billed_By_id=serializer.data[i]['Invoice_Billed_By'])
                BT1=Billed_To.objects.filter(Billed_To_id=serializer.data[i]['Invoice_Billed_To'])
                if len(user1)==0:
                    return HttpResponse("User Not Verified",status=status.HTTP_401_UNAUTHORIZED)
                # if len(client1)==0:
                #     return HttpResponse("No client detected",status=status.HTTP_401_UNAUTHORIZED)
                if len(BB1)==0:
                    return HttpResponse("Billed by not detected",status=status.HTTP_401_UNAUTHORIZED)
                if len(BT1)==0:
                    return HttpResponse("Billed to not detected",status=status.HTTP_401_UNAUTHORIZED)
                US=userSerializer(user1,many=True)
                #CS=clientSerializer(client1,many=True)
                BBS=Billed_BySerializer(BB1,many=True)
                BTS=Billed_BySerializer(BT1,many=True)
                # print(BTS.data,serializer.data[i]['Invoice_Billed_To'])
                # print(i)
                serializer.data[i]['Invoice_Billed_By']=BBS.data[0]
                serializer.data[i]['Invoice_Billed_To']=BTS.data[0]
                serializer.data[i]['user']=US.data[0]["user_username"]
                #serializer.data[i]['client']=CS.data[0]["client_name"]
                serializer.data[i]['Invoice_Billed_By'].pop('user_id')
                serializer.data[i]['Invoice_Billed_To'].pop('user_id')
                serializer.data[i].pop('user_id')
                #serializer.data[i].pop('client_id')
                # print(serializer.data[i]['Invoiceitems'])
                for j in range(len(serializer.data[i]['Invoiceitems'])):
                    
                    item1=items.objects.filter(item_id=serializer.data[i]['Invoiceitems'][j])
                    serializer1=itemsSerializer(item1,many=True)
                    serializer.data[i]['Invoiceitems'][j]=serializer1.data[0]
                    serializer.data[i]['Invoiceitems'][j].pop('user_id')
                    # print(serializer.data[i]['Invoiceitems'])
            # return Response(serializer.data)
            res=json.dumps(serializer.data)
            res=json.loads(res)
            return render(request,"invoices.html",context={'data':res})
        return HttpResponse("User Not Verified",status=status.HTTP_401_UNAUTHORIZED)
 
    def delete(self,request):
        inv_id=request.POST.dict()['invoice_id']
        # inv_id=request.data
        try:
            invoice1=Invoice.objects.get(invoice_id=inv_id)
            invoice2=Invoice.objects.filter(invoice_id=inv_id)
            # print(invoice2.values()[0]['user_id_id'])
            # print(invoice2[0].user_id_id)
            user_=user.objects.filter(user_id=invoice2[0].user_id_id)
            if len(user_)==0:
                return HttpResponse("No such invoice found",status=status.HTTP_404_NOT_FOUND)
            bil_by=invoice2[0].Invoice_Billed_By
            bil_to=invoice2[0].Invoice_Billed_To
            items=invoice2[0].Invoiceitems.all()
        except exceptions as e:
            return f'e'
        # print(invoice1,bil_by,bil_to,items)
        bil_by.delete()
        bil_to.delete()
        for item in items:
            item.delete()
        invoice1.delete()
        return redirect("http://127.0.0.1:8000/users/invoices/")

    def put(self,request):
        # print(request.data)
        try:
            inv=Invoice.objects.filter(invoice_id=request.data["invoice_id"])
            user1=user.objects.get(user_id=request.data["user_id"])
        except:
            return HttpResponse("Either Item is not found or user is not there",status=404)
        if request.user.email==user1.user_email:
            inv_li=inv_up_func(request.data)
            inv.update(**inv_li)
            if request.data["items"][0]!=0:
                for item in request.data["items"]:
                    inv[0].Invoiceitems.add(item)
        return HttpResponse("Item Updated!",status=status.HTTP_200_OK)


 

class clientsList(LoginRequiredMixin,APIView):
    login_url='/login/'
    def get(self,request):
        user1=client.objects.all()
        serializer=clientSerializer(user1,many=True)
        return Response(serializer.data)

def start(request):
    if request.user.is_authenticated:
        return redirect(home,msg=0)
    else:
        return redirect(home,msg=1)

def home(request,msg):
    print(msg)
    context={"msg":msg}
    return render(request,"home.html",context)

class index(LoginRequiredMixin,APIView):
    login_url='/login/'
    def get(self,request):
        form = InvoiceForm()
        context = {"form": form}
        return render(request, 'invoice.html', context)
        # if request.method == "POST":
        #     form = InvoiceForm(request.POST)
        #     if form.is_valid():
        #         form.save()
        #         print(request.POST["title"])
        #         # save FPDF() class into a
        #         # variable pdf
        #         pdf = FPDF()

        #         # Add a page
        #         pdf.add_page()

        #         # set style and size of font
        #         # that you want in the pdf
        #         pdf.set_font("Arial", size=15)

        #         # create a cell
        #         pdf.cell(200, 10, txt=request.POST["title"],
        #                  ln=20, align='C')

        #         # add another cell
        #         pdf.cell(200, 10, txt=request.POST["billed_by"],
        #                  ln=2, align='C')
        #         pdf.cell(200, 10, txt=request.POST["billed_to"],
        #                  ln=2, align='C')
        #         pdf.cell(200, 10, txt=request.POST["amount"],
        #                  ln=2, align='C')

        #         # save the pdf with name .pdf
        #         title = request.POST["title"]
        #         title = title + '.pdf'
        #         pdf.output(title)

        #         with open(title, "rb") as image_file:
        #             encoded_string = base64.b64encode(image_file.read())
        #         conn = http.client.HTTPSConnection("api.mailazy.com")
        #         recipients_list = [request.POST["email"]]
        #         recipients_list = json.dumps(recipients_list)
        #         # payload = (
        #         #     f"""{{  "to": {recipients_list}, 
        #         #             "from": "Sender@flookup.co.in", 
        #         #             "subject": {request.POST["title"]}, 
        #         #             "content": [{{
        #         #                     "type": "text/plain",
        #         #                     "value": "Hello Mr. {request.POST["billed_to"]}. Invoice of Rs. {request.POST["amount"]} generated by Mr. {request.POST["billed_by"]}  "
        #         #                     }}]
                            
        #         #             }}""")
        #         payload = (
        #             f"""{{  "to": ["ibupatra@gmail.com"], 
        #                     "from": "Sender@flookup.co.in", 
        #                     "subject": "{request.POST['title']}", 
        #                     "content": [{{
        #                             "type": "text/plain",
        #                             "value": "Hello Mr. {request.POST["billed_to"]}.\n Invoice of Rs. {request.POST["amount"]} generated by Mr. {request.POST["billed_by"]}  "
        #                             }}],
        #                     "attachments": [{{
        #                             "type": "application/pdf",
        #                             "file_name": "{title}",
        #                             "content": {encoded_string}
        #                     }}],
        #                     }}""")
        #         print(payload)
        #         headers = {
        #             'X-Api-Key': 'c7hf4l2dc007534ff8qgEHjqQUiSsj',
        #             'X-Api-Secret': ' FSjYwMfBDJlUXBUAttOtGBmfjvUOuBrwMEiuhYNd.WDWYxiTw2Zj6dh42TxSfPD',
        #             'Content-Type': 'application/json'
        #         }
        #         conn.request("POST", "/v1/mail/send", payload, headers)
        #         res = conn.getresponse()
        #         data = res.read()
        #         print(data.decode("utf-8"))
        
##########################################################################################################################################################

from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
# from xhtml2pdf import pisa

# def render_to_pdf(template_src, context_dict={}):
# 	template = get_template(template_src)
# 	html  = template.render(context_dict)
# 	result = BytesIO()
# 	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
# 	if not pdf.err:
# 		return HttpResponse(result.getvalue(), content_type='application/pdf')
# 	return None


data = {
	"company": "Dennnis Ivanov Company",
	"address": "123 Street name",
	"city": "Vancouver",
	"state": "WA",
	"zipcode": "98663",


	"phone": "555-555-2345",
	"email": "youremail@dennisivy.com",
	"website": "dennisivy.com",
	}

#Opens up page as PDF
class ViewPDF(View):
	def get(self, request, *args, **kwargs):

		pdf = render_to_pdf('pdf_template.html', data)
		return HttpResponse(pdf, content_type='application/pdf')


#Automaticly downloads to PDF file
class DownloadPDF(View):
	def get(self, request, *args, **kwargs):
		
		pdf = render_to_pdf('pdf_template.html', data)
		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "Invoice_%s.pdf" %("12341231")
		content = "attachment; filename='%s'" %(filename)
		response['Content-Disposition'] = content
		return response



##################################### Code by Abhiram ################################################################

class open_inv(LoginRequiredMixin,APIView):
    login_url='/login/'
    def get(self,request):
        edit=int(request.GET.dict()["Open/edit"])
        print(edit)
        if edit==0:
            return render(request,"invoice_receipt.html",context={"edit":0})
        else:
            # inv_id=request.GET.dict()["invoice_id"]
            API_ENDPOINT="http://127.0.0.1:8000/userinvoicelist/"
            try:
                header = {
                'X-CSRFToken':request.GET.dict()['csrfmiddlewaretoken'],
                'Content-Type': 'application/json',
                'Cookie': request.headers["Cookie"]
                }
                r=requests.get(url = API_ENDPOINT,data=json.dumps(request.GET.dict()),headers=header)
                data=json.loads(r.content.decode('UTF-8'))
                data[0]['item_count']=len(data[0]['Invoiceitems'])
                line=Html_parser(data[0]['Invoiceitems'])
                # print(data)
                # print(data)
            except exceptions as e:
                print(f"Invoice Getting Exception:{e}")
                return HttpResponse("Failed!!",status=status.HTTP_400_BAD_REQUEST)
        return render(request,"invoice_receipt.html",context={"invoice":data[0],"html":line,"edit":1})

    def post(self,request):
        res=info_parser(request.data.dict())
        json_data=json.dumps(res)
        header = {
        'X-CSRFToken':res['csrfmiddlewaretoken'],
        'Content-Type': 'application/json',
        'Cookie': request.headers["Cookie"]
        }
        # print(res['edit'])
        if int(res['edit'])==0:
            # print('hi')
            # print(res)
            API_ENDPOINT="http://127.0.0.1:8000/comp_invoice/"
            try:
                r=requests.post(url = API_ENDPOINT,data=json_data,headers=header)
            except exceptions as e:
                print(f"Invoice Posting Exception:{e}")
                return HttpResponse("Failed!!",status=status.HTTP_400_BAD_REQUEST)
        else:
            API_ENDPOINT="http://127.0.0.1:8000/comp_invoice/"
            try:
                r=requests.request("PUT",url = API_ENDPOINT,data=json_data,headers=header)
            except exceptions as e:
                print(f"Invoice Posting Exception:{e}")
                return HttpResponse("Failed!!",status=status.HTTP_400_BAD_REQUEST)
        return redirect("http://127.0.0.1:8000/users/invoices/")


class PDF(LoginRequiredMixin,APIView):
    login_url='/login/'
    def post(self,request):
        # print('hi')
        if type(request.data)!=dict:
            rem=0
            data=request.data.dict()
        else:
            rem=1
            data=request.data
        # print(data)
        API_ENDPOINT="http://127.0.0.1:8000/userinvoicelist/"
        try:
            header = {
            'X-CSRFToken':data['csrfmiddlewaretoken'],
            'Content-Type': 'application/json',
            'Cookie': request.headers["Cookie"]
            }
            r=requests.get(url = API_ENDPOINT,data=json.dumps(data),headers=header)
            data=json.loads(r.content.decode('UTF-8'))
        except exceptions as e:
            print(f"Invoice Posting Exception:{e}")
            return HttpResponse("Failed!!",status=status.HTTP_400_BAD_REQUEST)
        config = pdfkit.configuration(wkhtmltopdf = r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
        template = get_template('Edit_Invoice.html')
        html = template.render({'inv': data[0]})
        if rem==0:
            options = {
            'encoding': "UTF-8",
            }
            pdf = pdfkit.from_string(html, False, options,configuration = config)
            # with open('readme.pdf', 'wb+') as f:
            #     f.write(pdf)
            # print(f)
            # f.close()
            # os.remove('readme.pdf')
            print('hi')
            response = HttpResponse(pdf, content_type='application/pdf')
            filename=f'{data[0]["invoice_title"]}.pdf'
            response['Content-Disposition'] = f'attachment; filename={filename}'
            return response
        else:
            return HttpResponse(html, content_type="text/plain")
#################### SEND EMAILS API ########################
##################### This api sends mails to any number of people at the same time with attachments #################

class Send_Email(LoginRequiredMixin,APIView):
    login_url='/login/'
    def post(self,request):
        json_data = request.data
        connection = mail.get_connection()   # Use default email connection
        messages = get_notification_email(json_data)  # accessing the get_notification_email function in utils.py file
        connection.send_messages(messages)   # Sending many emails at the same time
        return HttpResponse("Emails Sent!!",status=status.HTTP_200_OK)

#################### SEND INVOICE BACKEND ########################
################ This api will call all other small api's that in turn actually send the invoice to its respective backend tables #######################################

class Comp_Invoice(LoginRequiredMixin,APIView):
    login_url='/login/'
    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, *args, **kwargs):
        # print("fsad")
        method = self.request.POST.get('_method', '').lower()
        # print(self.request,self.request.POST)
        if method == 'put':
            # print('hfaiofhew')
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(Comp_Invoice, self).dispatch(*args, **kwargs)


    def post(self,request):
        user1=user.objects.get(user_email__iexact=request.user.email)
        # print(request.data,'hi',type(request.data))
        request.data.update({"user_id":user1.user_id})
        # print(request.data)
        head=request.headers
        # print(head)
        ################ Calling the Billed_BY API #####################

        try:
            API_ENDPOINT = "http://127.0.0.1:8000/billed_by/"
            r = requests.post(url = API_ENDPOINT, data=json.dumps(request.data),headers=head)
            # print(r)
            data=json.loads(r.content.decode('UTF-8'))
            # print(data)
            request.data.update({"bil_by_id":data["Billed_By_id"]})
            # print('bil_by')
        except exceptions as e:
            print(f"Billed_By exception:{e}")
            return HttpResponse("Failed!!",status=status.HTTP_400_BAD_REQUEST)

        ################ Calling the Billed_To API #####################

        try:
            API_ENDPOINT = "http://127.0.0.1:8000/billed_to/"
            r = requests.post(url = API_ENDPOINT,data=json.dumps(request.data),headers=head)
            data=json.loads(r.content.decode('UTF-8'))
            request.data.update({"bil_to_id":data["Billed_To_id"]})
        except exceptions as e:
            print(f"Billed_To exception:{e}")
            return HttpResponse("Failed!!",status=status.HTTP_400_BAD_REQUEST)

        ################ Calling the items API #####################

        try:
            #user1=user.objects.get(user_email=request.user.email)
            API_ENDPOINT = "http://127.0.0.1:8000/users/items/"
            r = requests.post(url = API_ENDPOINT, data=json.dumps(request.data),headers=head)
            data=json.loads(r.content.decode('UTF-8'))
            print(data)
            request.data.update({"items":[x['item_id'] for x in data]})
            #request.data.update({"items":data})
        except exceptions as e:
            print(f"items exception:{e}")
            return HttpResponse("Failed!!",status=status.HTTP_400_BAD_REQUEST)

        ################ Calling the Invoice API #####################

        try:
            API_ENDPOINT = "http://127.0.0.1:8000/users/invoices/"
            r = requests.post(url = API_ENDPOINT, data=json.dumps(request.data),headers=head)
        except exceptions as e:
            print(f"Invoice exception:{e}")
            return HttpResponse("Failed!!",status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse("Success!!",status=status.HTTP_200_OK)

    def put(self,request):
        # print('hi')
        # print(request.data)
        user1=user.objects.filter(user_email__iexact=request.user.email)
        invoice_id=request.data["invoice_id"]
        # print(invoice_id)
        criterion1 = Q(invoice_id=invoice_id)
        criterion2 = Q(user_id=user1[0].user_id)
        invoice=Invoice.objects.filter(criterion1 & criterion2)
        bil_by_id=invoice[0].Invoice_Billed_By.Billed_By_id
        bil_to_id=invoice[0].Invoice_Billed_To.Billed_To_id
        item_ids=[x.item_id for x in invoice[0].Invoiceitems.all()]
        if invoice:
            request.data.update({"user_id":user1[0].user_id,"bil_by_id":bil_by_id,"bil_to_id":bil_to_id,
                                "item_ids":item_ids,"invoice_id":invoice_id})
            head=request.headers
            ################ Calling the Billed_BY API #####################

            try:
                API_ENDPOINT = "http://127.0.0.1:8000/billed_by/"
                r = requests.put(url = API_ENDPOINT, json=request.data,headers=head)
                # data=json.loads(r.content.decode('UTF-8'))
                # request.data.pop("bil_by_id")
            except exceptions as e:
                print(f"Billed_By exception:{e}")
                return HttpResponse("Failed!!",status=status.HTTP_400_BAD_REQUEST)

            ################ Calling the Billed_To API #####################

            try:
                API_ENDPOINT = "http://127.0.0.1:8000/billed_to/"
                r = requests.put(url = API_ENDPOINT,json=request.data,headers=head)
                # data=json.loads(r.content.decode('UTF-8'))
                # request.data.update({"bil_to_id":data["Billed_To_id"]})
            except exceptions as e:
                print(f"Billed_To exception:{e}")
                return HttpResponse("Failed!!",status=status.HTTP_400_BAD_REQUEST)

            ################ Calling the items API #####################

            try:
                #user1=user.objects.get(user_email=request.user.email)
                API_ENDPOINT = "http://127.0.0.1:8000/users/items/"
                r = requests.put(url = API_ENDPOINT, json=request.data,headers=head)
                if r.status_code==206:
                    data=json.loads(r.content.decode('UTF-8'))
                    # print(data)
                    request.data.update({"items":[x['item_id'] for x in data]})
                else:
                    request.data.update({"items":[0]})
            except exceptions as e:
                print(f"items exception:{e}")
                return HttpResponse("Failed!!",status=status.HTTP_400_BAD_REQUEST)

            ################ Calling the Invoice API #####################

            try:
                API_ENDPOINT = "http://127.0.0.1:8000/users/invoices/"
                r = requests.put(url = API_ENDPOINT, json=request.data,headers=head)
            except exceptions as e:
                print(f"Invoice exception:{e}")
                return HttpResponse("Failed!!",status=status.HTTP_400_BAD_REQUEST)
            return HttpResponse("Success!!",status=status.HTTP_200_OK)
        else:
            return HttpResponse("No such Invoice Found!!",status=status.HTTP_404_NOT_FOUND)

#################### Remainder Emails API ########################

class rem_emails(LoginRequiredMixin,APIView):
    login_url='/login/'
    def get(self,request):
        inv_id=request.GET.dict()["invoice_id"]
        ind=request.headers['Cookie'].find("csrftoken=")
        fin=request.headers['Cookie'][ind+10:].find(";")
        fin+=ind+10
        csrfmiddlewaretoken=request.headers['Cookie'][ind+10:fin]
        data=request.GET.dict().copy()
        data['csrfmiddlewaretoken']=csrfmiddlewaretoken
        try:
            header = {
            'X-CSRFToken':csrfmiddlewaretoken,
            'Content-Type': 'application/json',
            'Cookie': request.headers["Cookie"]
            }
            API_ENDPOINT="http://127.0.0.1:8000/Print/"
            r=requests.post(url = API_ENDPOINT,data=json.dumps(data),headers=header)
        except exceptions as e:
            print(f"Invoice Posting Exception:{e}")
            return HttpResponse("Failed!!",status=status.HTTP_400_BAD_REQUEST)
        html=r.content.decode('UTF-8')
        names=[]
        for task in PeriodicTask.objects.all():
            if task.enabled:
                names.append(task.name)
            else:
                task_obj=PeriodicTask.objects.get(name__iexact=task.name)
                task_obj.delete()
        return render(request,"rem-email.html",context={'inv_id':inv_id,"names":names,"email_pdf":html})
        # return render(request,"temp.html")
    def post(self,request):
        json_data = request.data.dict()
        schedule, created = CrontabSchedule.objects.get_or_create(     # Creating a Cron object in the database under
            day_of_month=json_data['day'],                    # Crontabs.Crontabs describe the tasks datetime
            month_of_year=json_data['month'],                  # schedule
            day_of_week='*',
            hour = json_data['hour'],
            minute = json_data['minute'])
            
        task = PeriodicTask.objects.create(                        # Adding a periodic object in the database under 
            crontab=schedule,                                      # Periodic_Tasks.Periodic tasks describe the task
            name=json_data["task_name"],                        # details of when to perform,whether task is done or not etc;
            task='trial.tasks.rem_email',
            args = json.dumps([json_data]),
            one_off=False)
        return HttpResponse("Emails Sent!!",status=status.HTTP_200_OK)

class whatsapp_api(LoginRequiredMixin,APIView):
    login_url='/login/'

    http_method_names = ['get', 'post', 'put', 'delete']
    def dispatch(self, *args, **kwargs):
        if self.request.method=='POST':
            return self.post(*args, **kwargs)
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(whatsapp_api, self).dispatch(*args, **kwargs)

    def get(self,request):
        inv_id=request.GET.dict()["invoice_id"]
        ind=request.headers['Cookie'].find("csrftoken=")
        fin=request.headers['Cookie'][ind+10:].find(";")
        fin+=ind+10
        csrfmiddlewaretoken=request.headers['Cookie'][ind+10:fin]
        data=request.GET.dict().copy()
        data['csrfmiddlewaretoken']=csrfmiddlewaretoken
        try:
            header = {
            'X-CSRFToken':csrfmiddlewaretoken,
            'Content-Type': 'application/json',
            'Cookie': request.headers["Cookie"]
            }
            API_ENDPOINT="http://127.0.0.1:8000/Print/"
            r=requests.post(url = API_ENDPOINT,data=json.dumps(data),headers=header)
        except exceptions as e:
            print(f"Invoice Posting Exception:{e}")
            return HttpResponse("Failed!!",status=status.HTTP_400_BAD_REQUEST)
        html=r.content.decode('UTF-8')
        # print(html)
        names=[]
        for task in PeriodicTask.objects.all():
            if task.enabled:
                names.append(task.name)
            else:
                task_obj=PeriodicTask.objects.get(name__iexact=task.name)
                task_obj.delete()
        return render(request,"rem_whatsapp.html",context={'inv_id':inv_id,"names":names,"whatsapp_pdf":html})
        a=final_call()
        if a==1:
            return HttpResponse("Msg Sent Succesfully",status=status.HTTP_200_OK)
        return HttpResponse("Msg Not Sent",status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        json_data = request.POST.dict()
        schedule, created = CrontabSchedule.objects.get_or_create(     # Creating a Cron object in the database under
            day_of_month=json_data['day'],                    # Crontabs.Crontabs describe the tasks datetime
            month_of_year=json_data['month'],                  # schedule
            day_of_week='*',
            hour = json_data['hour'],
            minute = json_data['minute'])
            
        task = PeriodicTask.objects.create(                        # Adding a periodic object in the database under 
            crontab=schedule,                                      # Periodic_Tasks.Periodic tasks describe the task
            name=json_data["task_name"],                        # details of when to perform,whether task is done or not etc;
            task='trial.tasks.rem_whatsapp',
            args = json.dumps([json_data]),
            one_off=False)
        return HttpResponse("Msg Sent!!",status=status.HTTP_200_OK)

        print('hi this is post')
        # print(request.data)
        print(request.POST)
        print(request.FILES,"file")
        print(request.headers)
        # print(request.data,"data")
        # print(request.FILES,"file")
        # print(request.FILES)
        return 123

################### User Login API ####################################


class log_auth(APIView):
    def get(self,request):
        if request.user.is_anonymous:
            return render(request,"Login.html")
        else:
            return HttpResponse("User is already Logged in",status=status.HTTP_401_UNAUTHORIZED)
    def post(self,request):
        json_data = request.data
        print(json_data)
        name=json_data['username']
        pwd=json_data['password']
        if "@" not in name:
            user=authenticate(username=name,password=pwd)
            if user is not None:
                login(request, user)
                return redirect(home,msg=0)
            else:
                return HttpResponse("Pls sign up first",status=status.HTTP_401_UNAUTHORIZED)
        else:
            user=User.objects.get(email__iexact=name)
            if user:
                login(request, user)
                return redirect(home,msg=0)
            else:
                return HttpResponse("Pls sign up first",status=status.HTTP_401_UNAUTHORIZED)


################### User Sign_in API ####################################


class sign_in(APIView):
    def get(self,request):
        return render(request,'signup.html')

    def post(self,request):
        json_data = request.data
        json_data=json_data.dict()
        first_name=json_data['first_name']
        last_name=json_data['last_name']
        username=json_data['username']
        password=json_data['password']
        email=json_data['email']
#        user=authenticate(username=username,password=password)
        user = User.objects.filter(email__iexact=email) | User.objects.filter(username__iexact=username)
        if len(user)==0:
            ########################## Don't Use this since it's not encrypting the password ##################


            serializer=AuthSerializer(data=json_data)                              
            if serializer.is_valid():
                user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name,last_name=last_name)
                user.save()


            ########################## Don't Use this since it's not encrypting the password ##################
            
            user = User.objects.filter(username__iexact=username)
            Data={"email_ver_OTP":'None',"email_verified":False,
                  "auth_id":user[0].id,"pass_change_OTP":'None'
                    }
            serializer=OtpSeraializer(data=Data)
            if serializer.is_valid():
                serializer.save()
            try:
                API_ENDPOINT = "http://127.0.0.1:8000/OTP/"
                otp_res= requests.get(url = API_ENDPOINT, json=request.data)
            except exceptions as e:
                print(f"Auth exception:{e}")
            if otp_res.status_code==200:
                return render(request,"otp-ver.html",context={"user_id":user[0].id})
            else:
                try:
                    API_ENDPOINT = f"http://127.0.0.1:8000/sign_in/"
                    delete_res = requests.delete(url = API_ENDPOINT, json=user[0].username)
                except exceptions as e:
                    print(f"Auth exception:{e}")
                return HttpResponse("Email Not Verified",status=status.HTTP_401_UNAUTHORIZED)
        else:

            return HttpResponse("User with the same email or username already present",status=status.HTTP_401_UNAUTHORIZED)
    def delete(self,request):
        try:
            auth_obj= User.objects.get(username__iexact=request.data)
        except:
            return HttpResponse("Authentication Object Deletion Error",status=404)
        auth_obj.delete()
        try:
            us_obj=user.objects.get(username__iexact=request.data)
        except:
            return HttpResponse("User Object Deletion Error",status=404)
        us_obj.delete()
        return HttpResponse("User Deleted!",status=status.HTTP_204_NO_CONTENT)

################### User Logout API ####################################


class log_out(LoginRequiredMixin,APIView):
    login_url='/login/'
    def get(self,request):
        try:
            logout(request)
        except exceptions as e:
            print(f'logout exception {e}')
        return redirect(home,msg=1)

################### User Auth API ####################################

class auth(APIView):
    def post(self,request):
        print(request.data)
        if 'username' in request.data.keys():
            if '@' in request.data['username']:
                email=request.data['username']
                user1=User.objects.filter(email__iexact=email)
            else:
                username=request.data['username']
                user1=User.objects.filter(username__iexact=username)
        elif 'email' in request.data.keys():
            if '@' in request.data['email']:
                email=request.data['email']
                user1=User.objects.filter(email__iexact=email)
            else:
                username=request.data['email']
                user1=User.objects.filter(username__iexact=username)
        else:
            return HttpResponse("Credentials are not entered correct",status=status.HTTP_401_UNAUTHORIZED)
            
        if len(user1)==0:
            return HttpResponse("User not found",status=status.HTTP_401_UNAUTHORIZED)
        else:
            if len(user1.values('email'))==0:
                return HttpResponse("Email Not Added",status=status.HTTP_401_UNAUTHORIZED)
            else:
                return HttpResponse("User found",status=status.HTTP_200_OK)

################### User OTP_VERIFICATION API ####################################

class OTP_ver(APIView):
    def get(self,request):
        json_data=request.data
        if len(json_data)==0:
            json_data=request.GET
            json_data=json_data.dict()
        try:
            API_ENDPOINT = "http://127.0.0.1:8000/auth/"
            auth_res = requests.post(url = API_ENDPOINT, json=json_data)
        except exceptions as e:
            print(f"Auth exception:{e}")
        if auth_res.status_code==200:
            otp=otpgen(json_data['email'])
            user = User.objects.filter(email__iexact=json_data['email'])
            user1 = User_OTP.objects.filter(auth_id=user[0].id)
            if user1.values('email_verified')[0]['email_verified']==False:
                now=timezone.make_aware(datetime.now(),pytz.UTC)
                user1.update(ver_OTP_time=now)
                #print(otp)
                user1.update(email_ver_OTP=otp)
            else:
                now=timezone.make_aware(datetime.now(),pytz.UTC)
                user1.update(pass_OTP_time=now)
                user1.update(pass_change_otp=otp)
                return render(request,"otp-ver.html",context={"user_id":user[0].id})
            user_data=Dict_Key_Changer(json_data,"user_",1,0)
            user_data["auth_id"]=user[0].id
            serializer=userSerializer(data=user_data)
            if serializer.is_valid():
                serializer.save()
            return HttpResponse("OTP Sent",status=status.HTTP_200_OK)
    def post(self,request):
        json_data=request.data
        json_data=json_data.dict()
        ############# ADD email variable when redirecting to page ###################
        user = User.objects.filter(id=json_data['user_id'])
        user1 = User_OTP.objects.filter(auth_id=user.values('id')[0]['id'])       
        if user1.values('email_verified')[0]['email_verified']==True:
            then=user1.values('pass_OTP_time')[0]['pass_OTP_time']
            now = timezone.make_aware(datetime.now(),pytz.UTC)
            pass_timediff_val=now-then
            if pass_timediff_val.total_seconds()/60<=10:
                if json_data['otp']==user1.values('pass_change_otp')[0]['pass_change_otp']:
                    return render(request,"Confirm_Password.html",context={"user_id":json_data['user_id']})
                else:
                    return HttpResponse("OTP not Verified",status=status.HTTP_401_UNAUTHORIZED)
            else:
                return HttpResponse("OTP Timeout",status=status.HTTP_401_UNAUTHORIZED)
        elif json_data['otp']==user1.values('email_ver_OTP')[0]['email_ver_OTP']:
            then=user1.values('ver_OTP_time')[0]['ver_OTP_time']
            now = timezone.make_aware(datetime.now(),pytz.UTC)
            ver_timediff_val=now-then
            if ver_timediff_val.total_seconds()/60<=10:
                user1.update(email_verified=True)
                user1.update(ver_OTP_time=None)
                user1.update(email_ver_OTP=None)
                return redirect(home,msg=2)
            else:
                try:
                    user1.delete()
                    API_ENDPOINT = f"http://127.0.0.1:8000/sign_in/{user.values('id')[0]['id']}"
                    delete_res = requests.delete(url = API_ENDPOINT, json=json_data)
                except exceptions as e:
                    print(f"Auth exception:{e}")
                return HttpResponse("OTP Timeout",status=status.HTTP_401_UNAUTHORIZED)
        else:
            return HttpResponse("OTP not Verified",status=status.HTTP_401_UNAUTHORIZED)

################### User Forgot Password API ####################################

class Forgot_pass(APIView):
    def get(self,request):
        if request.user.is_authenticated==False:
            return render(request,"Email_Verification.html")
        else:
            return HttpResponse("You are Already Logged_in, Logout and try again",status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def post(self,request):
        if request.data["new_password"]==request.data["confirm_password"]:
            user1 = User_OTP.objects.filter(auth_id=request.data['user_id'])
            user = User.objects.get(id=request.data['user_id'])
            if not user.check_password(request.data["confirm_password"]):
                user1.update(pass_change_otp=None)
                user1.update(pass_OTP_time=None)
                user.set_password(request.data["confirm_password"])
                user.save()
                return redirect(home,msg=2)
            else:
                return HttpResponse("Old password",status=status.HTTP_401_UNAUTHORIZED)
        else:
            return HttpResponse("Pls enter same password in both fields",status=status.HTTP_401_UNAUTHORIZED)