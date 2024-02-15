from rest_framework import serializers
from MS1_web.models import user



class UserSerializer(serializers.Serializer):
    class Meta:
        model = user
        fields = '__all__'
class ProfileSerializer(serializers.Serializer):
    username = serializers.CharField( max_length=255)
    email = serializers.CharField(max_length=255)
    legal_name = serializers.CharField(max_length=255)
    pfp = serializers.ImageField()
    phone = serializers.CharField( max_length=11)  # The composite primary key (phone, username, email, pw) found, that is not supported. The first column is selected.
    pw = serializers.CharField(max_length=255)
