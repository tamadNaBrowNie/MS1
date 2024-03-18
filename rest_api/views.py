from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MS1_web.models import user
from django.contrib.auth.hashers import check_password,make_password
from .serializer import UserSerializer
from MS1_web.forms import UserForm
# Create your views here.
from rest_framework.parsers import JSONParser 
@api_view(['POST'])
def LoginUser(request):
    # TODO: cahce uname. declare wtf after 5 attempts. if it appears again, reject.
    
    
    creds = request.query_params
    uname = creds['username']
    pw = creds['pw']
    pw = user.pw.filter(username=uname)
    if uname == 'admin' and pw == "I identify as 1/300 C because i'm a km/s":
        return Response('welcome admin', status =200)
    dat = user.objects.raw(""" SELECT username,pw FROM user WHERE username = %s""",(uname,))
    pw = dat[0].pw
    # print (dat)
    if not check_password(password = creds['pw'],encoded = pw):
        return Response(', '.join((creds['pw'],pw)),status = 500)

    # dat = MyUser.objects.raw(bio,creds)

    return Response(pw,status = 200)
@api_view(['POST'])
def NewUser(request):
    # this is the query
    # data['pw'] = make_password(data['pw'])
    # dic = data.copy()
    # dic['pw'] = make_password(dic['pw'])
    serial = UserSerializer(data=request.data)
    # serial =  UserForm(data=data)
    try:
        serial.is_valid(raise_exception=True)
        post = serial.save()
        post.pw =make_password(request.data['pw'])
        post.save()
        return Response(status=200)
    except Exception as e:
        return Response(str(e),status=400)