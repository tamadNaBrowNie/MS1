import logging
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
# from .models import User
from .forms import *
from .models import user,doc
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from rest_api.serializer import UserSerializer
from MS1.settings import DEBUG
from MS1.myerrs import DeadSessionException,timeout
from django_middleware_fileuploadvalidation.decorators import file_upload_config
from django.http import HttpResponseForbidden
# Create your views here.
def reg(request):
    request.session.flush()
    return render(request, 'reg.html', {'form':UserForm()})

def login(request): 
    return render(request, 'login.html',{'form': LoginForm()})
def land(req):
    req.session.flush()
    return render(req, 'land.html')
logger = logging.getLogger('actions')
def home(req): 
    try:
        timeout(req)
  
        ldb = logging.getLogger('django.db')
        ls = logging.getLogger('django.contrib.sessions')
        
        data = req.session['data']
        logger = logging.getLogger('auth')
        ldb = logging.getLogger('django.db')
        ls = logging.getLogger('django.contrib.sessions')
        logger.info(data['name']+' successfully entered')
        return render(req,'home.html',{'form':SearchForm(),**data,'pfp_form':ChangePfp(),'pw_form':ChangePw,'doc_form':DocForm,'finder_form':SearchDoc})
    except DeadSessionException as e:
        req.session.clear_expired()
        return redirect('entry')
    except Exception as e:
        if DEBUG: raise e
        else: return render(req, 'err.html',{'err':'An error happened','t':50,'url':''})

# @file_upload_config(
#   file_size_limit=2000000,
#   keep_original_filename=True,
#   response_config={
#       "error_func": HttpResponseForbidden,
#       "message": "Please upload a document.",
#       "status": 403,
#   },
#   whitelist= [
#     "image/jpeg",   # JPEG
#     "image/png",    # PNG
#     "image/gif",    # GIF
#     "image/bmp",    # BMP
#     # "image/webp"    # WebP
# ]

# )
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

def newPFP(req):
   try:
        if req.method != 'POST':
            return redirect('home')
        name = req.session['data']['name']
        rec =user.objects.get(pk=name)
        # form =  ChangePfp(req.POST, req.FILES, instance=rec)
        # fname = req.FILES
        # logger.info(f'{name} changed pfp')
        
        logger.info(f'{name} tries adding {req.FILES}')
        # logger.info(f'{name} changed{form.is_valid()}')
        rec =user.objects.get(pk=name)
        file = req.FILES.get('pfp')
        rec.pfp = file
        rec.save()
        # print(form.is_valid())
        # if form.is_valid():
        #     form.save()
        #     logger.info(f'{name} changed{req.FILES["pfp"]}')
        
        serial = UserSerializer(rec)
        req.session['data'] =  {
                'name':serial.data['username'],
                'img':serial.data['pfp'],
                'phone':serial.data['phone'],
                'email':serial.data['email']
                }
        return redirect('home')
   except Exception as e:
        if DEBUG:
            raise e
            # return render(req, 'err.html',{'err':req.FILES,'t':50,'url':''})

        else: return render(req, 'err.html',{'err':'An error happened','t':50,'url':''})


def to_admin(request):

    if not request.session['is_admin']:
        logger.info('invalid admin entry')
        return HttpResponseNotFound("<h1>Page not found</h1>")
    
    logger.info('valid admin entry')
    users = user.objects.all().values()
    docs = doc.objects.all().values()
    return render(request, 'admin.html',{'name_form':ChangeName,'users':users,'docs':docs})

def rmUser(request, username):
    if not request.session['is_admin']:
        logger.info('invalid admin entry')
        return HttpResponseNotFound("<h1>Page not found</h1>")
    mem = user.objects.get(pk=username)
    logger.info(f'admin removing {mem}')
    mem.delete()
    return redirect('admin')
def rmDoc(request, ind):
    if not request.session['is_admin']:
        logger.info('invalid admin entry')
        return HttpResponseNotFound("<h1>Page not found</h1>")
    mem = doc.objects.get(pk=ind)
    logger.info(f'admin removing {mem}')
    mem.delete()
    return redirect('admin')

@file_upload_config(
  file_size_limit=2000000,
  keep_original_filename=True,
  response_config={
      "error_func": HttpResponseForbidden,
      "message": "Please upload a document.",
      "status": 403,
  },
  whitelist= 
  [

    'text/plain',
    'application/msword',  # .doc
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # .docx
    'application/vnd.ms-excel',  # .xls
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # .xlsx
    'application/vnd.ms-powerpoint',  # .ppt
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',  # .pptx
    'application/pdf',
    'application/vnd.oasis.opendocument.text',  
    'application/vnd.oasis.opendocument.spreadsheet', 
    'application/vnd.oasis.opendocument.presentation',  
    'application/x-freearc',
    'application/epub+zip'
]

)
def DocX(req):
   try:
        if 'data' not in req.session:
           raise TimeoutError
        name = req.session['data']['name']
        if req.method != 'POST':
            return redirect('home')
        logger.info(f'{name} tries adding')
        form = DocForm(req.POST, req.FILES)
        if form.is_valid():
            logger.info(f'{name} added {req.FILES} to docs')
            post= form.save()

        return redirect('home')
   except Exception as e:
        if DEBUG: raise e
        else: return render(req, 'err.html',{'err':'An error happened','t':50,'url':''})
def leave(req):
    req.session.flush()
    return redirect('landing')
