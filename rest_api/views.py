from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MS1_web.models import MyUser
from django.contrib.auth.hashers import check_password
# Create your views here.

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
    dat = MyUser.objects.raw(cred,[uname])
    print (dat)
    # if not check_password(password = creds['pw'],encoded = dat['pw']):pass
    #     return Response(status = 500)

    # dat = MyUser.objects.raw(bio,creds)

    return Response(status = 200)
@api_view(['POST'])
def NewUser(request):
    # this is the query
    add= """INSERT INTO user (username, email,legal_name,pfp,phone,pw) VALUES(%(uName)s,%(email)s,%(name)s,%(pfp)s,%(num)s,%(pw)s)"""
    return Response('foo',status=200)