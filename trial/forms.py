from django.forms import ModelForm
from trial.models import user
from trial.models import Invoice


# class UserForm(ModelForm):
#      class Meta:
#          model = user
#          exclude=('auth_id',)
#          fields = [
#     "username":"Random2",
#     "password":"test1234",
#     "email":"abhiramganesh98@gmail.com",
#     "first_name":"xyz",
#     "last_name":"abc",
#     "company":"abc limited"
# ]

class InvoiceForm(ModelForm):
     class Meta:
         model = Invoice
         fields = '__all__'