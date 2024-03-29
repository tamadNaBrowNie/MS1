"""
URL configuration for MS1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from  .views import *

urlpatterns = [
   path('register/',reg, name ='register'),
    path('',land,name = 'landing'),
    path('login/',login,name='entry'),
    path('home/',home,name='home'),
    path('home/pfp/',newPFP),
    path('admin/',to_admin,name ='admin'),
    path('admin/delete/user/<str:username>',rmUser,name ='rmU'),
    path('admin/delete/doc/<int:ind>',rmDoc,name ='rmD'),
    path('home/doc/',DocX),
     path('admin/leave',leave), path('home/leave',leave),
    
]
