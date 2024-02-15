from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MS1_web.models import MyUser
from django.contrib.auth.hashers import check_password
# Create your views here.

@api_view(['GET'])
def LoginUser(request):
    
    cred = """
    SELECT pw FROM user WHERE user.username = %(username)s LIMIT 1; 
               """

    
    bio =    """
    SELECT username, email,legal_name, pfp, phone FROM user WHERE user.username = %(username)s ; 
                 """
    creds = request.query_params
    dat = MyUser.objects.raw(cred,creds)[0]
    if not check_password(password = creds['pw'],encoded = dat['pw']):
        return Response(status = 500)

    dat = MyUser.objects.raw(bio,creds)
    return Response(dat,status = 200)
@api_view(['POST'])
def NewUser(request):
    # this is the query
    add= """INSERT INTO user (username, email,legal_name,pfp,phone,pw) VALUES(%(uName)s,%(email)s,%(name)s,%(pfp)s,%(num)s,%(pw)s)"""
    return Response('foo',status=200)