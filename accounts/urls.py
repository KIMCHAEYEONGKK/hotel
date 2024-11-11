from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from accounts.views import signup, login, logout


app_name = 'accounts'

urlpatterns =[
    path('signup/',views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # path('signup/idCheckForm/',views.idCheck, name='idCheck'),
    path('signup/idCheckProc/',views.idCheck, name='idProc'),
    path('home/',views.home, name="home")

]