
from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
# from file_validator.models import DjangoFileValidator
def post(instance, filename):return f"doc/{instance.ind}/{instance.title}/{filename}"
class doc(models.Model):
    ind =  models.AutoField(primary_key=True)
    title = models.CharField(max_length=255,null = False)
    file = models.FileField(blank=True, null=True,  upload_to= 'doc/'
                            # upload_to=post,
                            )
    # def file(self):return self._file
    class Meta:
        managed = False
        db_table = 'posts'

def pfp(instance, filename): return f"{instance.username}/pfp/{filename}"
class user(models.Model):
    last_login = None
    username = models.CharField(primary_key=True,unique=True, max_length=16)
    email = models.EmailField(required=True,max_length=255)
    legal_name = models.CharField(equired=True,max_length=255)
    pfp = models.ImageField(required=False,allow_empty_file=True,blank=True, null=True,
                            upload_to= pfp,                            # allow_empty=True
                           )
    phone = models.CharField(required=True,max_length=11,) 
    password = models.CharField(max_length=255,validators=[
            RegexValidator(
                r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{16,255}$',
                message="Password length is 16-255. Has upper case and lower case English letter, special character, and numbers. "
            )])
    

    class Meta:
        managed = False
        db_table = 'user'
        unique_together = (('phone', 'username', 'email'),)
