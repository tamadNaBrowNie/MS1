from rest_framework import serializers
from MS1_web.models import User

import re
# pw_v=[
#             RegexValidator(
#                 regex=r'^(09|)\d{9}$',
#                 message="Invalid Number ",
#                 code="invalid password",
#             ),
#         ]
# ph_v =[
#             RegexValidator(
#                 regex=r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{16,255}$',
#                 message="Password is 16-255 characters long with atleast one upper case English letter, one lower case English letter, one special character ",
#                 code="invalid password",
#             ),
#         ]
class UserSerializer(serializers.ModelSerializer):
    def validate_pw(self,value):
        username = serializers.CharField( max_length=255)
        email = serializers.CharField(max_length=255)
        legal_name = serializers.CharField(max_length=255)
        pfp = serializers.ImageField()
        phone = serializers.CharField( max_length=11)
        pw = serializers.CharField(max_length=255)
        regex = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{16,255}$')    # Pattern Modified from https://ihateregex.io/expr/password/

        if not regex.match(value):
            raise serializers.ValidationError("Password length is 16-255. Has upper case and lower case English letter, special character, and numbers. ")
        return value
    def validate_phone(self,value):
        regex = re.compile(r'^(09|)\d{9}$')
        if not regex.match(value):
            raise serializers.ValidationError("Invalid Philippine Cellphone")
        return value
    class Meta:
        model = User
        fields = '__all__'
class ProfileSerializer(serializers.Serializer):
    pass
