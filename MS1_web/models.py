# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
def thumb(instance, filename):return f"{instance.title}/img/{filename}"
def doc(instance, filename):return f"{instance.title}/doc/{filename}"
class entry(models.Model):
    ind =  models.AutoField(primary_key=True)
    owner = models.ForeignKey(to='user', on_delete=models.RESTRICT)
    thumb = models.ImageField(blank=True, null=True, upload_to=thumb)
    doc = models.FileField(blank=True, null=True,   upload_to=doc )
    title = models.CharField(max_length=255,null = False)
    class Meta:
        managed = False
        db_table = 'posts'

def pfp(instance, filename): return f"{instance.username}/pfp/{filename}"
class user(AbstractBaseUser):
    last_login = None
    username = models.CharField(primary_key=True,unique=True, max_length=255)
    email = models.EmailField(max_length=255)
    legal_name = models.CharField(max_length=255)
    pfp = models.ImageField(blank=True, null=True,
                            upload_to= pfp
                           )
    phone = models.CharField(max_length=11,) 
    password = models.CharField(max_length=255,)
    

    class Meta:
        managed = False
        db_table = 'user'
        unique_together = (('phone', 'username', 'email'),)
