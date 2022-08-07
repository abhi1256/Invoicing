from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.db.models.fields import EmailField
from django.utils.translation import ugettext_lazy as _

from listview.views import approvals


# Create your models here.
class CustomBaseManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, username, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address.'))
        email = self.normalize_email(email)
        user = self.model(email = email, username = username, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=False)
    email = models.EmailField(_('email address'), unique=True)
    approvals = models.IntegerField(default= 0 ,null=True)
    company = models.CharField(max_length=50,  default="None", null=False )
    phone = models.CharField(max_length=50, default="None", null=False )
    
    first_name = None
    last_name = None
    date_joined = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomBaseManager()

    def __str__(self):
        return self