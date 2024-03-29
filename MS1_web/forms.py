from django.forms import ModelForm,CharField,PasswordInput,ImageField,EmailField,FileField
from .models import user,doc

class UserForm(ModelForm):
    email = EmailField(required=True,max_length=255)
    legal_name = CharField(required=True,max_length=255)
    pfp = ImageField(required=False,allow_empty_file=True,                       # allow_empty=True
                           )
    phone = CharField(required=True,max_length=11,) 
    password =CharField(required=True, max_length=255, widget=PasswordInput,label='Password',
                  )
    repeat_password =CharField(required=True, max_length=255, widget=PasswordInput)

    
    class Meta:
        model = user
        fields = '__all__'

class SearchForm(ModelForm):
    class Meta:
        model = user
        fields = ['username']
class SearchDoc(ModelForm):
    class Meta:
        model = doc
        fields = ['title']
class LoginForm(ModelForm):
    password =CharField(required=True, max_length=255, widget=PasswordInput,label='Password',)
    class Meta:
        model = user
        fields = ['username','password']
# def pfp(instance, filename): return f"{instance.username}/pfp/{filename}"    
class DocForm(ModelForm):
    title =CharField(max_length=255,required=True)
    file = FileField(required=True,allow_empty_file=True,  )
    class Meta:
        model = doc
        fields =['title','file']
class ChangePfp(ModelForm):
    # pfp = ImageField(required=False,allow_empty_file=True,)                       # allow_empty=True
    class Meta:
        model = user
        fields = ['pfp']
class ChangePw(ModelForm):
    old =CharField(required=True, max_length=255, widget=PasswordInput,label='Old Password',)
    new =CharField(required=True, max_length=255, widget=PasswordInput,label='New Password', )
    again =CharField(required=True, max_length=255, widget=PasswordInput,label='Repeat Password',)
    class Meta:
        model = user
        fields = []
class ChangeName(ModelForm):
        class Meta:
            model = user
            fields = ['username','legal_name']