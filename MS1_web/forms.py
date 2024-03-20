from django.forms import ModelForm,CharField,PasswordInput,ImageField,EmailField,FileField
from .models import user,doc

# ^(09|)\d{9}$
class UserForm(ModelForm):
    username =CharField(required=True, max_length=16)
    password =CharField(required=True, max_length=255, widget=PasswordInput,label='Password',
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
class SearchDoc(ModelForm):
    class Meta:
        model = doc
        fields = ['title','owner']
class LoginForm(ModelForm):
    password =CharField(required=True, max_length=255, widget=PasswordInput,label='Password',)
    class Meta:
        model = user
        fields = ['username','password']
def pfp(instance, filename): return f"{instance.username}/pfp/{filename}"    
class DocForm(ModelForm):
# The lines `ind = AutoField()` and `owner = ForeignKey()` in the `DocForm` class are defining fields
# for the `doc` model form.
    # ind =  AutoField()
    # owner = ForeignKey()
    title =CharField(max_length=255,required=True)
    file = FileField(required=False,allow_empty_file=True  )
    class Meta:
        model = doc
        fields =['title','file']
class ChangePfp(ModelForm):
    def is_valid(self) -> bool:
        return True
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
        