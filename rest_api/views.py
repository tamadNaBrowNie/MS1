from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MS1_web.models import User
from django.contrib.auth.hashers import check_password
# Create your views here.

@api_view(['GET'])
def LoginUser(request):
    
    cred = """
    SELECT pw FROM user WHERE user.username = %(name)s LIMIT 1; 
               """

    
    bio =    """
    SELECT username, email,legal_name, pfp, phone FROM user WHERE user.username = %(name)s ; 
                 """
    dat = User.objects.raw(cred,args)[0]
    if not check_password(password = args['pw'],encoded = dat['pw']):
        return Response(status = 500)
    args = request.query_params
    dat = User.objects.raw(bio,args)
    return Response(dat,status = 200)
def NewUser(request):
    add= """INSERT INTO user (username, email,legal_name,pfp,phone,pw) VALUES(%(uName)s,%(email)s,%(name)s,%(pfp)s,%(num)s,%(pw)s)"""