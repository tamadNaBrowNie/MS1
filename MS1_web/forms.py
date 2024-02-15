from django.forms import ModelForm,CharField,PasswordInput,ImageField,EmailField
from .models import MyUser
class UserForm(ModelForm):
    username =CharField(required=True, max_length=16)
    pw =CharField(required=True, max_length=255, widget=PasswordInput,label='Password')
    repeat_password =CharField(required=True, max_length=255, widget=PasswordInput)
    email = EmailField(required=True, max_length=255)
    legal_name = CharField(required=True, max_length=255)
    pfp = ImageField()
    phone = CharField(required=True, max_length=11) 
    
    class Meta:
        model = MyUser
        fields = '__all__'

