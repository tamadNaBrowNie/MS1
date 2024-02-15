# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class User(models.Model):
    username = models.CharField(unique=True, max_length=16)
    email = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255)
    pfp = models.TextField(blank=True, null=True)
    phone = models.CharField(primary_key=True, max_length=11)  # The composite primary key (phone, username, email, pw) found, that is not supported. The first column is selected.
    pw = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'user'
        unique_together = (('phone', 'username', 'email', 'pw'),)
