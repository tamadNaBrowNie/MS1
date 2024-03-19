from django.forms import ModelForm,CharField,PasswordInput,ImageField,EmailField,ValidationError,FileField
from .models import user,entry
# ^(09|)\d{9}$
class UserForm(ModelForm):
    username =CharField(required=True, max_length=16)
    pw =CharField(required=True, max_length=255, widget=PasswordInput,label='Password',
                  )
    repeat_password =CharField(required=True, max_length=255, widget=PasswordInput)
    email = EmailField(required=True, max_length=255)
    legal_name = CharField(required=True, max_length=255)
    pfp = ImageField(required=False,allow_empty_file=True)
    phone = CharField(required=True, max_length=11,) 
    
    class Meta:
        model = user
        fields = '__all__'
    # def clean_passwords(self,*args,**kwargs):
    #     pw = self.cleaned_data['pw']
    #     repeat_password = self.clean_data['repeat_password']
    #     if pw != repeat_password:
    #         raise ValidationError('Password mismatch')
    #     else: return pw
class SearchForm(ModelForm):
    class Meta:
        model = user
        fields = ['username']
class LoginForm(ModelForm):
    pw =CharField(required=True, max_length=255, widget=PasswordInput,label='Password',)
    class Meta:
        model = user
        fields = ['username','pw']
        
class Archive(ModelForm):
    title = CharField(required=True, max_length=255)
    thumb = ImageField(required=False, )
    doc = FileField(required=False,)
    class Meta:
        model = entry
        fields = '__all__'
