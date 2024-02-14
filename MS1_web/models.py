# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Credentials(models.Model):
    uid = models.PositiveIntegerField(primary_key=True)  # The composite primary key (uid, username) found, that is not supported. The first column is selected.
    username = models.CharField(unique=True, max_length=16)
    pw = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'credentials'
        unique_together = (('uid', 'username'),)


class User(models.Model):
    username = models.CharField(unique=True, max_length=16)
    email = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255)
    pfp = models.TextField(blank=True, null=True)
    joined = models.DateField()
    uuid = models.AutoField(primary_key=True)  # The composite primary key (uuid, username, email, legal_name) found, that is not supported. The first column is selected.

    class Meta:
        managed = False
        db_table = 'user'
        unique_together = (('uuid', 'username', 'email', 'legal_name'),)
