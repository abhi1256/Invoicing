from django.contrib import admin
from django.urls import path,include
from trial import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("",views.start),
    path("<int:msg>/",views.home),
    path("index/",views.index.as_view()),
    path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
    path('userlist/',views.usersList.as_view()),
    path('clients/',views.clientsList.as_view()),
    path('items/',views.itemsList.as_view()),
    path('billed_by/',views.billed_by.as_view()),
    path('billed_to/',views.billed_to.as_view()),
    path('invoices/',views.invoiceList.as_view()),
    path('userinvoicelist/',views.User_invoiceList.as_view()),
    path('users/',views.userDetails.as_view()),
    path('users/items/',views.userItems.as_view()),
    path('users/clients/',views.userClients.as_view()),
    path('users/invoices/',views.userInvoices.as_view()),
    path('email/',views.Send_Email.as_view()),
    path('comp_invoice/',views.Comp_Invoice.as_view()),
    path('Rem/',views.rem_emails.as_view()),
    path('login/',views.log_auth.as_view()),
    path('sign_in/',views.sign_in.as_view()),
    path('logout/',views.log_out.as_view()),
    path('auth/',views.auth.as_view()),
    path('forgot/',views.Forgot_pass.as_view()),
    path('OTP/',views.OTP_ver.as_view()),
    path('Open_Invoice/',views.open_inv.as_view()),
    path('Print/',views.PDF.as_view()),
    path('whatsapp_api/',views.whatsapp_api.as_view())
]
