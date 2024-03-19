
from django.contrib.auth.backends import BaseBackend
from MS1_web.models import User
from settings import ADMIN_LOGIN
from django.core.exceptions import ObjectDoesNotExist
class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        # Your custom authentication logic goes here
        # For example, you might want to authenticate against an external API
        # Replace this with your actual authentication logic
        # login_admin = settings.ADMIN_LOGIN == Username
        # pw = "I identify as 1/300000*C because I'm a km/s"
        # pw_admin = password == pw
        try:
            User = User.objects.get(pk=username)
            if User.check_password(password):
                return User
            else:
                return None
        except ObjectDoesNotExist:
            return None

    def get_User(self, user_id ):
        try:
            return  User.objects.get(pk=user_id )
        except ObjectDoesNotExist:
            return None
    def has_perm(self, user_obj, perm, obj=None): return user_obj.username == ADMIN_LOGIN