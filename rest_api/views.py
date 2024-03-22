import logging
from django.shortcuts import redirect
from rest_framework.serializers import ValidationError
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.response import Response
from MS1_web.models import user,doc
from django.contrib.auth.hashers import check_password,make_password
from .serializer import UserSerializer,DocSerializer
from MS1_web.forms import DocForm
from rest_framework.renderers import TemplateHTMLRenderer,BrowsableAPIRenderer
# Create your views here.
from rest_framework.parsers import JSONParser 
from django.core.exceptions import ObjectDoesNotExist
import re
from MS1.settings import DEBUG
from MS1.myerrs import DeadSessionException,timeout
from django.http import HttpResponseForbidden

from django_middleware_fileuploadvalidation.decorators import file_upload_config

@api_view(['POST'])
def newName(req):
    try:
        uname = req.data['username']
        name = req.data['legal_name']
        rec =user.objects.get(pk=uname)
        rec.legal_name = name
        rec.save()
        req.session['is_admin'] = True
        return redirect('admin')
    except ObjectDoesNotExist as e: 
            return Response({'err':'Unmatched user','t':3},status=400,template_name = 'err.html')
    except Exception as e:
        if not DEBUG:return Response({'err':'Error occured','t':5,'url':''}, status=500,template_name='err.html',)
        raise e
log = logging.getLogger('actions')
@api_view(['POST'])
def newPW(req):

    name = 'a user'
    try:
        timeout(req)
        name = req.session['data']['name']
        
        rec =user.objects.get(pk=name)
        if not check_password(password = req.data['old'],encoded = rec.password):
            raise ValueError('Not Password')
        regex = re.compile('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{16,255}$')    # Pattern Modified from https://ihateregex.io/expr/password/

        # if not regex.match(req.data['new']):
        #     raise ValidationError("Password length is 16-255. Has upper case and lower case English letter, special character, and numbers. ")
        if req.data['new'] != req.data['again']:
            raise ValueError('Mismatched Passwords')
        rec.password = make_password(req.data['new'])
        rec.save()
        log.info(f'{name} changed password from{req.data["old"]} to {req.data["new"]}')
        return redirect('home')
    except (ValueError,ValidationError) as e:
        log.info(f'{name} failed password change reason: {str(e)}')
        return Response({'err':str(e),'t':3,'url':'home'},status=400,template_name = 'err.html')
    except DeadSessionException as e:
        log.info(f'{name} timed out')
        return Response({'err':'dead session','t':3,'url':'entry'},status=400,template_name = 'err.html')
    except Exception as e:
        if DEBUG: raise e
        else: return Response({'err':'Error occured'+'DNE','t':5,'url':''}, status=500,template_name='err.html',)

@api_view(['POST'])
@renderer_classes([TemplateHTMLRenderer,])
def LoginUser(request):

    creds = request.data
    uname = creds['username']
   
    if uname == 'admin' and creds['password'] == "I identify as 1/300 C because i'm a km/s":
        log.info('admin is entering')
        request.session['is_admin'] = True
        return redirect('admin')
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
            raise ObjectDoesNotExist
        request.session['data']=data
        request.session['auth']=make_password(uname)
        log.info(f'{data["name"]} is entering')
        return redirect('home',)
    except ObjectDoesNotExist as e: 
        log.info(f'failed login')
        return Response({'err':'Unmatched user','t':3},status=400,template_name = 'err.html')
    except Exception as e:
        log.info(f'broken login')
        if not DEBUG:return Response({'err':'Error occured','t':5,'url':''}, status=500,template_name='err.html',)
        raise e

# @api_view(['POST'])
@file_upload_config(
  file_size_limit=2000000,
  keep_original_filename=True,
  response_config={
      "error_func": HttpResponseForbidden,
      "message": "Please upload a document.",
      "status": 403,
  },
  whitelist= [
    "image/jpeg",   # JPEG
    "image/png",    # PNG
    "image/gif",    # GIF
    "image/bmp",    # BMP
    "image/webp"    # WebP
]

)
@api_view(['POST'])
@renderer_classes([TemplateHTMLRenderer,BrowsableAPIRenderer])
def NewUser(request):
    
    
    try:
        if request.data['username'] == 'admin':
            raise ValidationError
        serial = UserSerializer(data=request.data)
        serial.is_valid(raise_exception=True)
        if request.data['password'] != request.data['repeat_password']:
            raise ValidationError('Unmatched Passwords')
        post = serial.save()
        post.password =make_password(request.data["password"])
        post.save()
        log.info(f'welcome {serial.data["username"]}')
        return redirect('entry')
    except ValidationError as e:
            log.info('user registration failed')
            # if DEBUG: raise e
            return Response({'err':e,'t':20},status=400,template_name = 'err.html')
    
    except Exception as e:
            log.info('registration broke')
            if DEBUG: raise e
            else: return Response({'err':'Error?','t':10,'url':''}, status=500,template_name='err.html',)
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def SeeUser(request):
    param = request.query_params
    try:
        log.info(f'{request.session["data"]["name"]} searched for {param["username"]}')
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
        return Response({'err':' '.join((param['username'],'DNE')),'t':100,'url':'home'},status=400,template_name = 'err.html')
    except Exception as e:
        if DEBUG: raise e
        else: return Response({'err':'Error?','t':5,'url':''}, status=500,template_name='err.html',)
@api_view(['POST'])
def newName(req):
    param = req.data
    rec =user.objects.get( username=param['username'])
    rec.legal_name = param['legal_name'] 
    rec.save()
    log.info(f"admin changed{param['username']}'s legal name to {param['legal_name']}")
    return redirect('admin')
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def findDoc(req):
    param = req.query_params
    rec =doc.objects.filter( title=param['title'])
    # log.info(f"admin changed{param['username']}'s legal name to {param['legal_name']}")
    return Response({'lst':rec,'t':100,'url':'home'},status=400,template_name = 'docs.html')
# @api_view(['POST'])
# def DocX(req):
#    try:
#         if 'data' not in req.session:
#            raise TimeoutError
#         name = req.session['data']['name']
#         serial = DocSerializer(data=req.data)
#         serial.is_valid(raise_exception=True)
#         serial.save()
#         log.info(f'{name} tries adding {req.raw_post_data}')
#         # form = DocForm(req.POST, req.FILES)
#         # if form.is_valid():
#         #     log.info(f'{name} added {req.FILES} to docs')
#         #     post= form.save()

#         return redirect('home')
#    except Exception as e:
#         if DEBUG: raise e
#         else: return Response({'err':'Error?','t':5,'url':''}, status=500,template_name='err.html',)
#         # else: return render(req, 'err.html',{'err':'An error happened','t':50,'url':''})