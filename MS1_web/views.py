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
# Create your views here.
def reg(request):
    return render(request, 'reg.html', {'form':UserForm()})

def login(request): 
    return render(request, 'login.html',{'form': LoginForm()})
def land(req): return render(req, 'land.html')

def home(req): 
    try:
        data = req.session['data']
        logger = logging.getLogger('auth')
        logger.info(f'{data['name']} successfully entered')
        return render(req,'home.html',{'form':SearchForm(),**data,'pfp_form':ChangePfp(),'pw_form':ChangePw,'doc_form':DocForm,'finder_form':SearchDoc})
    except KeyError as e:
        if DEBUG: raise e
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
        if form.is_valid():
            form.save()
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
    return render(request, 'admin.html',{'name_form':ChangeName,'users':users})

def delete(request, username):
    if not request.session['is_admin']:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    mem = user.objects.get(pk=username)
    mem.delete()
    return redirect('admin')
  

# return render(req,'make.html',{'form':Archive()})
# def hello(request):
#     return HttpResponse('Hello')
def DocX(req):
   try:
        if req.method != 'POST':
            return redirect('home')

        form = DocForm(req.POST, req.FILES)
        if form.is_valid():
           post= form.save()
        # rec.pfp = f'{name}/pfp/{req.FILES['pfp'].name}'
        # # rec.pfp = req.data['pfp']
        # rec.save()
    
        # form = ChangePfp(req.POST,req.FILES,instance = rec)
        # if not form.is_valid():
        #     return redirect("/home")
        # form.save()
        # rec =user.objects.get(pk= req.session['data'] ['name'])
        # serial = UserSerializer(rec)
        # req.session['data'] =  {
        #         'name':serial.data['username'],
        #         'img':serial.data['pfp'],
        #         'phone':serial.data['phone'],
        #         'email':serial.data['email']
        #         }
        return redirect('home')
   except Exception as e:
        if DEBUG: raise e
        else: return render(req, 'err.html',{'err':'An error happened','t':50,'url':''})
