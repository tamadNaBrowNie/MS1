from rest_framework import serializers
from MS1_web.models import user
from MS1_web import models


class UserSerializer(serializers.Serializer):
    class Meta:
        model = user
        fields = '__all__'
class ProfileSerializer(serializers.Serializer):
    username = serializers.CharField(unique=True, max_length=16)
    email = serializers.CharField(max_length=255)
    legal_name = serializers.CharField(max_length=255)
    pfp = serializers.TextField(blank=True, null=True)
    phone = serializers.CharField(primary_key=True, max_length=11)  # The composite primary key (phone, username, email, pw) found, that is not supported. The first column is selected.
    pw = models.CharField(max_length=255)
