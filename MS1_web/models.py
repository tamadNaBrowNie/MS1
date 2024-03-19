# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class entry(models.Model):
    ind =  models.AutoField(primary_key=True)
    owner = models.ForeignKey(to='user', on_delete=models.RESTRICT)
    thumb = models.ImageField(blank=True, null=True,
                                upload_to=
                            lambda instance, filename: f"{instance.title}/img/{filename}")
    doc = models.FileField(blank=True, null=True,   upload_to=
                            lambda instance, filename: f"{instance.title}/doc/{filename}")
    title = models.CharField(max_length=255,null = False)
    class Meta:
        managed = False
        db_table = 'posts'


class user(models.Model):
    username = models.CharField(primary_key=True,unique=True, max_length=255)
    email = models.EmailField(max_length=255)
    legal_name = models.CharField(max_length=255)
    pfp = models.ImageField(blank=True, null=True,
                            upload_to=
                            lambda instance, filename: f"{instance.username}/pfp/{filename}")
    phone = models.CharField(max_length=11,) 
    pw = models.CharField(max_length=255,)
    

    class Meta:
        managed = False
        db_table = 'user'
        unique_together = (('phone', 'username', 'email'),)
