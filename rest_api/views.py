from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MS1_web.models import user
from django.contrib.auth.hashers import check_password,make_password
from .serializer import UserSerializer
# Create your views here.
from rest_framework.parsers import JSONParser 
@api_view(['GET'])
def LoginUser(request):
    
    cred = """
    SELECT pw, username FROM user WHERE username = %s; 
               """

    
    bio =    """
    SELECT username, email,legal_name, pfp, phone FROM user WHERE user.username = %(name)s ; 
                 """
    
    creds = request.query_params
    uname = request.query_params['username']
    # pw = user.pw.filter(username=uname)
    dat = user.objects.filter(username=uname)
    pw = dat[0].pw
    # print (dat)
    if not check_password(password = request.query_params['pw'],encoded = pw):
        return Response(status = 500)

    # dat = MyUser.objects.raw(bio,creds)

    return Response(pw,status = 200)
@api_view(['POST'])
def NewUser(request):
    # this is the query
    data = request.data
    # data['pw'] = make_password(data['pw'])
    dic = data.copy()
    dic['pw'] = make_password(dic['pw'])
    serial = UserSerializer(data= dic)
    if serial.is_valid():
        serial.save()
        return Response(serial.data,status=200)
    return Response('bar',status=400)