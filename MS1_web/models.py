
from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator

def post(instance, filename):return f"{instance.title}/doc/{filename}"
class doc(models.Model):
    owner_id = None
    ind =  models.AutoField(primary_key=True)
    owner = models.ForeignKey(to='user', on_delete=models.CASCADE, related_name='entries')
    file = models.FileField(blank=True, null=True,   upload_to=post )
    title = models.CharField(max_length=255,null = False)

    class Meta:
        managed = False
        db_table = 'posts'

def pfp(instance, filename): return f"{instance.username}/pfp/{filename}"
class user(models.Model):
    last_login = None
    username = models.CharField(primary_key=True,unique=True, max_length=255)
    email = models.EmailField(max_length=255)
    legal_name = models.CharField(max_length=255)
    pfp = models.ImageField(blank=True, null=True,
                            upload_to= pfp,
                            validators=[
            RegexValidator(
                r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{16,255}$',
                message="Password length is 16-255. Has upper case and lower case English letter, special character, and numbers. "
            )
        ]
                            # allow_empty=True
                           )
    phone = models.CharField(max_length=11,) 
    password = models.CharField(max_length=255,)
    

    class Meta:
        managed = False
        db_table = 'user'
        unique_together = (('phone', 'username', 'email'),)
