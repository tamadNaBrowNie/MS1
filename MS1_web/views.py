from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
# from .models import User
from .forms import UserForm,LoginForm,ChangePfp,SearchForm,ChangePw
from django.contrib.auth.decorators import login_required

# Create your views here.
def reg(request):
    return render(request, 'reg.html', {'form':UserForm()})

def login(request): 
    return render(request, 'login.html',{'form': LoginForm()})
def land(req): return render(req, 'land.html')
# @login_required
def home(req): 
    try:
        data = req.session['data']
    except KeyError:
        return redirect('entry')
    #TODO: UPLOADE DOC, CHANGE PFP, CHANGE PW, DELETE DOC then done with 5 cruds and doc upload
    return render(req,'home.html',{'form':SearchForm(),**data,'pfp_form':ChangePfp(),'pw_form':ChangePw})
def make(req):pass
# return render(req,'make.html',{'form':Archive()})
# def hello(request):
#     return HttpResponse('Hello')