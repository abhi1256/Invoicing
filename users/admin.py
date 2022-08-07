from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from users.forms import CustomUserCreationForm

from .models import CustomUser

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(DjangoUserAdmin):

    model = CustomUser
    add_form = CustomUserCreationForm


# admin.site.register(CustomUser, CustomUserAdmin)