from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from .models import user
from .forms import UserForm,LoginForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def reg(request):
    form = UserForm()
    context = {'form':form}
    return render(request, 'reg.html',context)
@login_required
def login(request):
    form = LoginForm()
    context = {'form':form}
    return render(request, 'login.html',context)
def land(req):
    return render(req, 'land.html')
# def hello(request):
#     return HttpResponse('Hello')