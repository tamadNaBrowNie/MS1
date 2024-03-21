
from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
from file_validator.models import DjangoFileValidator
def post(instance, filename):return f"{instance.owner}/doc/{instance.title}/{filename}"
class doc(models.Model):
    owner_id = None
    ind =  models.AutoField(primary_key=True)
    owner = models.ForeignKey(to='user', on_delete=models.CASCADE, related_name='entries',to_field = 'username')
    title = models.CharField(max_length=255,null = False)
    file = models.FileField(blank=True, null=True,   upload_to="doc/",
                            validators=[
            # DjangoFileValidator(
            #     libraries=["python_magic", "filetype",'mimetypes'], 
            #     acceptable_mimes=
            #     ['application/msword',
            #      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            #      'application/epub+zip','application/vnd.oasis.opendocument.spreadsheet',
            #      'application/vnd.oasis.opendocument.spreadsheet',
            #      'application/vnd.oasis.opendocument.text',
            #      'application/pdf',
            #      'application/vnd.ms-powerpoint',
            #      'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            #      'text/plain',
            #      'application/vnd.ms-excel',
            #      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            #      ], 
            #     # acceptable_types=['text', 'application', ], 
            #     max_upload_file_size=10485760  # => 10 MB
            # )
            ] 
            )
    # def file(self):return self._file
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
                            upload_to= pfp,                            # allow_empty=True
                           )
    phone = models.CharField(max_length=11,) 
    password = models.CharField(max_length=255,validators=[
            RegexValidator(
                r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{16,255}$',
                message="Password length is 16-255. Has upper case and lower case English letter, special character, and numbers. "
            )])
    

    class Meta:
        managed = False
        db_table = 'user'
        unique_together = (('phone', 'username', 'email'),)
