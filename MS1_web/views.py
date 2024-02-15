from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from .models import MyUser
from .forms import UserForm
# Create your views here.
def reg(request):
    form = UserForm()
    context = {'form':form}
    return render(request, 'reg.html',context)
def login(request):
    return render(request, 'login.html')
def land(req):
    return render(req, 'land.html')
# def hello(request):
#     return HttpResponse('Hello')