from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from .models import user
from .forms import UserForm,LoginForm,Archive
from django.contrib.auth.decorators import login_required

# Create your views here.
def reg(request):
    return render(request, 'reg.html', {'form':UserForm()})

def login(request): 
    return render(request, 'login.html',{'form': LoginForm()})
def land(req): return render(req, 'land.html')
@login_required
def home(req): return render(req,'home.html',{'form':Archive()})
def make(req):return render(req,'make.html')
# def hello(request):
#     return HttpResponse('Hello')