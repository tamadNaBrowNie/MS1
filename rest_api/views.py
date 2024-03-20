from django.shortcuts import redirect
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.response import Response
from MS1_web.models import user
from django.contrib.auth.hashers import check_password,make_password
from .serializer import UserSerializer
from MS1_web.forms import UserForm
from rest_framework.renderers import TemplateHTMLRenderer
# Create your views here.
from rest_framework.parsers import JSONParser 
from django.core.exceptions import ObjectDoesNotExist
# from backends.base.SessionBase import get_session_cookie_age
@api_view(['POST'])
def LoginUser(request):

    creds = request.data
    uname = creds['username']
   

        

    if uname == 'admin' and creds['password'] == "I identify as 1/300 C because i'm a km/s":
        return Response('welcome admin', status =200)
    try:
        rec =user.objects.get(pk=uname)
        serial = UserSerializer(rec)
        data = {
        'name':serial.data['username'],
        'img':serial.data['pfp'],
        'phone':serial.data['phone'],
        'email':serial.data['email']
        }
        if not check_password(password = request.data['password'],encoded = serial.data['password']):
            return Response(serial.data,status=400,template_name = 'land.html')
        request.session['data']=data
        request.session['auth']=make_password(uname)
        return redirect('home',)
    except ObjectDoesNotExist: 
        return redirect('entry')
    

@api_view(['POST'])
def NewUser(request):
    
    serial = UserSerializer(data=request.data)
    try:
        valid = serial.is_valid(raise_exception=True)
        if not valid: raise Exception(str(serial.errors))
        # if request.data['password'] != request.query_params['password']:
        #     raise Exception('Passwords unmatching')
        post = serial.save()
        post.password =make_password(request.data['password'])
        post.save()
        return redirect('entry')
    except Exception as e:
        return Response({'err':str(e)},status=400,template_name = 'err.html')
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def SeeUser(request):
    param = request.query_params
    rec =user.objects.get( pk=param['username'])
    serial = UserSerializer(rec)
    
    data = {
        'name':serial.data['username'],
        'img':serial.data['pfp'],
        'phone':serial.data['phone'],
        'email':serial.data['email']
        }
    return Response(data,status=200,template_name = 'user.html')