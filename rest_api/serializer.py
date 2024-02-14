from rest_framework.serializers import Serializer
from MS1_web.models import user
from MS1_web import models


class UserSerializer(Serializer):
    class Meta:
        model = user
        fields = '__all__'
