# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.validators import RegexValidator

class user(models.Model):
    username = models.CharField(unique=True, max_length=255)
    email = models.EmailField(max_length=255)
    legal_name = models.CharField(max_length=255)
    pfp = models.BinaryField(blank=True, null=True, )
    phone = models.CharField(primary_key=True, max_length=11,validators=[
            RegexValidator(
                regex=r'^(09|)\d{9}$',
                message="Invalid Number ",
                code="invalid password",
            ),
        ],)  # The composite primary key (phone, username, email, pw) found, that is not supported. The first column is selected.
    pw = models.CharField(max_length=255,validators=[
            RegexValidator(
                regex=r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{16,255}$',
                message="Password is 16-255 characters long with atleast one upper case English letter, one lower case English letter, one special character ",
                code="invalid password",
            ),
        ],)
    # Pattern Modified from https://ihateregex.io/expr/password/
    

    class Meta:
        managed = False
        db_table = 'user'
        unique_together = (('phone', 'username', 'email', 'pw'),)
