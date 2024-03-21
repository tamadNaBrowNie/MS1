from rest_framework import serializers
from MS1_web.models import user,doc

import re

class DocSerializer(serializers.ModelSerializer):
    # owner = serializers.RelatedField(read_only=True,many=False)
    class Meta:
        model = doc
        fields = ['file','title']
class UserSerializer(serializers.ModelSerializer):
    def validate_password(self,value):
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
        model = user
        fields = '__all__'