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
    return render(req, 'err.html',{'err':'An error happened','t':50,'url':''})
    
def newPFP(req):
   try:
        if req.method != 'POST':
            return redirect('home')
        name = req.session['data']['name']
        rec =user.objects.get(pk=name)
        form =  ChangePfp(req.POST, req.FILES, instance=rec)
        logger.info(f'{name} changing pfp to {req.FILES['pfp'].name}')
        if form.is_valid():
            form.save()
            logger.info(f'{name} changed pfp to {req.FILES['pfp'].name}')
        # rec.pfp = f'{name}/pfp/{req.FILES['pfp'].name}'
        # # rec.pfp = req.data['pfp']
        # rec.save()
    
        # form = ChangePfp(req.POST,req.FILES,instance = rec)
        # if not form.is_valid():
        #     return redirect("/home")
        # form.save()
        rec =user.objects.get(pk=name)
        serial = UserSerializer(rec)
        req.session['data'] =  {
                'name':serial.data['username'],
                'img':serial.data['pfp'],
                'phone':serial.data['phone'],
                'email':serial.data['email']
                }
        return redirect('home')
   except Exception as e:
        if DEBUG: raise e
        else: return render(req, 'err.html',{'err':'An error happened','t':50,'url':''})


def to_admin(request):
    if not request.session['is_admin']:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    users = user.objects.all().values()
    docs = doc.objects.all().values()
    return render(request, 'admin.html',{'name_form':ChangeName,'users':users,'docs':docs})

def rmUser(request, username):
    if not request.session['is_admin']:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    mem = user.objects.get(pk=username)
    mem.delete()
    return redirect('admin')
def rmDoc(request, ind):
    if not request.session['is_admin']:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    mem = doc.objects.get(pk=ind)
    mem.delete()
    return redirect('admin')
  

# return render(req,'make.html',{'form':Archive()})
# def hello(request):
#     return HttpResponse('Hello')
@file_upload_config(
  file_size_limit=2000000,
  keep_original_filename=True,
  response_config={
      "error_func": HttpResponseForbidden,
      "message": "Please upload a document.",
      "status": 403,
  },
  whitelist= [
    # Text
    'text/plain',


    # Office Documents
    'application/msword',  # .doc
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # .docx
    'application/vnd.ms-excel',  # .xls
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # .xlsx
    'application/vnd.ms-powerpoint',  # .ppt
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',  # .pptx

    # PDF
    'application/pdf',

    # OpenDocument
    'application/vnd.oasis.opendocument.text',  # .odt
    'application/vnd.oasis.opendocument.spreadsheet',  # .ods
    'application/vnd.oasis.opendocument.presentation',  # .odp
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
        logger.info(f'{name} tries adding {req.FILES}')
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
