from django.forms import ModelForm,CharField,PasswordInput,ImageField,EmailField,ValidationError
from .models import MyUser
from django.core.validators import RegexValidator
class UserForm(ModelForm):
    username =CharField(required=True, max_length=16)
    pw =CharField(required=True, max_length=255, widget=PasswordInput,label='Password',validators=[
            RegexValidator(
                regex=r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{16,255}$',
                message="Password is 16-255 characters long with atleast one upper case English letter, one lower case English letter, one special character ",
                code="invalid password",
            ),
        ],)
    repeat_password =CharField(required=True, max_length=255, widget=PasswordInput)
    email = EmailField(required=True, max_length=255)
    legal_name = CharField(required=True, max_length=255)
    pfp = ImageField()
    phone = CharField(required=True, max_length=11) 
    
    class Meta:
        model = MyUser
        fields = '__all__'
    def clean_passwords(self,*args,**kwargs):
        pw = self.cleaned_data['pw']
        repeat_password = self.clean_data['repeat_password']
        if pw != repeat_password:
            raise ValidationError('Password mismatch')
        else: return pw
        