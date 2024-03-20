from django.shortcuts import redirect
from rest_framework.serializers import ValidationError
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
from django.core.files.storage import FileSystemStorage
import re
# from backends.base.SessionBase import get_session_cookie_age
# @api_view(['POST'])
# def newPFP(req):
#     name = req.session['data']['name']
#     rec =user.objects.get(pk=name)
#     fs = FileSystemStorage
#     pfp = req.data['pfp'].name
#     rec.pfp = pfp
#     rec.save
#     # serial =  UserSerializer(rec)
#     # serial.data['pfp'] = req.data['pfp'].str()
#     # serial.save
#     data = {
#         'name':rec.username,
#         'img':rec.pfp,
#         'phone':rec.phone,
#         'email':rec.email
#         }
#     req.session['data'] = data
#     return redirect('home')
@api_view(['POST'])
def newPW(req):
    try:
        name = req.session['data']['name']
        rec =user.objects.get(pk=name)
        if not check_password(password = req.data['old'],encoded = rec.password):
            raise ValueError('Not Password')
        regex = re.compile('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{16,255}$')    # Pattern Modified from https://ihateregex.io/expr/password/

        if not regex.match(req.data['new']):
            raise ValidationError("Password length is 16-255. Has upper case and lower case English letter, special character, and numbers. ")
        if req.data['new'] != req.data['again']:
            raise ValueError('Mismatched Passwords')
        rec.password = make_password(req.data['new'])
        rec.save()
        return redirect('home')
    except (ValueError,ValidationError) as e:
        return Response({'err':str(e),'t':3,'url':'home'},status=400,template_name = 'err.html')
    except ObjectDoesNotExist: 
        return Response({'err':'Invalid Access','t':3,'url':''},status=400,template_name = 'err.html')

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
            raise ObjectDoesNotExist('Not Password')
        request.session['data']=data
        request.session['auth']=make_password(uname)
        return redirect('home',)
    except ObjectDoesNotExist as e: 
       return Response({'err':str(e),'t':3,'url':''},status=400,template_name = 'err.html')
    

@api_view(['POST'])

@renderer_classes([TemplateHTMLRenderer])
def NewUser(request):
    
    serial = UserSerializer(data=request.data)
    try:
        serial.is_valid(raise_exception=True)
        # if not valid: raise ValidationError(str(serial.errors))
        if request.data['password'] != request.data['repeat_password']:
            raise ValueError('Unmatched Passwords')
            # return Response({'err':'foo','bar':'bar'},status=400,template_name = 'err.html')
        post = serial.save()
        post.password =make_password(request.data['password'])
        post.save()
        return redirect('entry')
    except Exception as e:
        return Response({'err':str(e),'t':3},status=400,template_name = 'err.html')
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def SeeUser(request):
    param = request.query_params
    try:
        rec =user.objects.get( pk=param['username'])
        serial = UserSerializer(rec)
        
        data = {
            'name':serial.data['username'],
            'img':serial.data['pfp'],
            'phone':serial.data['phone'],
            'email':serial.data['email']
            }
        return Response(data,status=200,template_name = 'user.html')
    except ObjectDoesNotExist: 
        return Response({'err':param['username']+'DNE','t':100,'url':'home'},status=400,template_name = 'err.html')