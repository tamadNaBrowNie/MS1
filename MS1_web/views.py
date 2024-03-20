from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
# from .models import User
from .forms import UserForm,LoginForm,ChangePfp,SearchForm,ChangePw,DocForm
from .models import user
from django.contrib.auth.decorators import login_required
from rest_api.serializer import UserSerializer

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
    return render(req,'home.html',{'form':SearchForm(),**data,'pfp_form':ChangePfp(),'pw_form':ChangePw,'doc_form':DocForm})
def newPFP(req):
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
    data = {
            'name':serial.data['username'],
            'img':serial.data['pfp'],
            'phone':serial.data['phone'],
            'email':serial.data['email']
            }
    req.session['data'] = data
    return redirect('home')

    


# return render(req,'make.html',{'form':Archive()})
# def hello(request):
#     return HttpResponse('Hello')