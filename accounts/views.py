import sqlite3
import threading

from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from flask import flash

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from accounts.forms import SignupForm, LoginForm
from django.contrib.auth import authenticate
from django.contrib import auth
from accounts.models import Account
from rest_framework.response import Response
from accounts.serializer import ContactSerializer

import re

MINIMUM_PASSWORD_LENGTH = 8
MINIMUM_USER_ID_LENGTH = 8

def validate_email(email):
    a = re.compile('^[a-zA-Z0-9-_.]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$')
    b = a.match(email)
    if b is None:
        return True
    else:
        return False

# def validate_is_email(email):
#     if Account.objects.filter(email=email).exists():
#         return True
#     else:
#         return False

def validate_id(user_id):
    if len(user_id) < MINIMUM_USER_ID_LENGTH:
        return False
    return True

def validate_password(password):
    if len(password) < MINIMUM_PASSWORD_LENGTH:
        return False
    return True

def validate_phone(phone):
    pattern = re.compile('^[0]\d{2}\d{3,4}\d{4}$')
    if not pattern.match(phone):
        return False
    return True
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            user_id = form.cleaned_data.get("user_id")
            password = form.cleaned_data.get("password")
            name = form.cleaned_data.get('name')
            password1 = form.cleaned_data.get("password1")
            eName1 = form.cleaned_data.get('eName1')
            eName2 = form.cleaned_data.get('eName2')
            gender = form.cleaned_data.get('gender')
            address = form.cleaned_data.get('address')
            email = form.cleaned_data.get('email')
            postcode = form.cleaned_data.get('postcode')
            detailAddress = form.cleaned_data.get('detailAddress')
            phone= form.cleaned_data.get('phone')


            # if Account.objects.filter(Q(user_id=user_id) | Q(email=email) | Q(phone=phone)):
            #     return JsonResponse({'message':'USER_ALREADY_EXISTS'}, status=409)


            # if not validate_email(email):
            #     return JsonResponse({'message': 'EMAIL_VALIDATION_ERROR'}, status=422)
            #
            # if not validate_password(password):
            #     return JsonResponse({'message': 'PASSWORD_VALIDATION_ERROR'}, status=422)
            #
            # if not validate_phone(phone):
            #     return JsonResponse({'message': 'PHONE_VALIDATION_ERROR'}, status=422)

            user = authenticate(user_id=user_id, password=password, name=name,phone=phone,
                                 address=address, postcode=postcode, detailAddress=detailAddress,password1=password1, eName1=eName1, eName2=eName2, gender=gender,email=email,
                                )
            # user = Account(user_id=user_id, password=password,name=name, password1=password1,eName1=eName1, eName2=eName2,gender=gender, address=address,postcode=postcode,detailAddress=detailAddress)
            auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend')


            return redirect('accounts:login')


    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html',{'form':form})



def checkemail(request):
    try:
        user = Account.objects.get(email=request.GET['email'])
    except Account.DoesNotExist:
        user = None
    result = {
        'result': 'success',
        # 'data' : model_to_dict(user)  # console에서 확인
        'data': "not exist" if user is None else "exist"
    }
    return JsonResponse(result)



# def idCheck(request):
#     try:
#         user_id = request.GET.get('user_id')
#     except MultiValueDictKeyError:
#         result = {'result': 'error', 'data': 'user_id parameter is missing'}
#         return JsonResponse(result, status=400)
#     try:
#         user=Account.objects.get(user_id=user_id)
#     except Account.DoesNotExist:
#         user = None
#     except ValueError:
#         result = {'result': 'error', 'data': 'Invalid user_id parameter'}
#         return JsonResponse(result, status=400)
#
#     result = {
#         'result': 'success',
#         # 'data' : model_to_dict(user)  # console에서 확인
#         'data': "not exist" if user is None else "exist"
#     }
#     # return render(request, 'accounts/idCheckProc.html',{'result':result})
#     return JsonResponse(result)

def idCheck(request):
    id = request.GET.get('id')
    print(id)

    if id in Account:
        eng='아이디가 이미 존재 합니다.'
    elif len(id)<8:
        eng='8자리 이상 입력하여야 합니다.'
    else:
        eng="사용 가능한 아이디입니다."

    context={'eng':eng}
    return JsonResponse(context)


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data.get('user_id')
            password = form.cleaned_data.get('password')
            user = authenticate(user_id=user_id, password=password)
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('accounts:home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

# def login(request):
#     if request.method =="POST":
#         user_id = request.POST['user_id']
#         password = request.POST['password']
#         user=auth.authenticate(user_id=user_id, password=password)
#         if user is not None:
#             auth.login(request, user)
#             return redirect('accounts:home')
#         else:
#             return render(request, 'accounts/login.html')
#     else:
#         return render(request, 'accounts/login.html')


def logout(request):
    if request.session.get('user'):
        del (request.session['user'])
    return redirect('accounts:login')

def home(request):
    return render(request,'accounts/home.html')