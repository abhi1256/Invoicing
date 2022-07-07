from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
# from django.core.exceptions import ObjectDoesNotExist

class CustomUserBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):

        custom_model = get_user_model()
        try:
            user = custom_model.objects.get(email = email)
            if user.check_password(password):
                return user
        except custom_model.DoesNotExist:
            return None

        return None

    def get_user(self, user_id):
        current_model = get_user_model()
        try:
            return current_model.objects.get(pk=user_id)
        except current_model.DoesNotExist:
            return None