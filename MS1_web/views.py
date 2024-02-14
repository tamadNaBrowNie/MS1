from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def reg(request):
    return render(request, 'reg.html')
def login(request):
    return render(request, 'login.html')
def land(req):
    return HttpResponse('Welcome')
# def hello(request):
#     return HttpResponse('Hello')