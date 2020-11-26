import json
import requests

from django.views import View
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import get_user_model
from .models import Member
from main.models import Product



def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')

def success(request):
    return render(request, "success.html")

def kakao_signup(request):
    login_request_uri = "https://kauth.kakao.com/oauth/authorize?"

    client_id = '9529fd434fd3250003c8cd727617a243'
    redirect_uri = 'http://127.0.0.1:8000/oauth'
    login_request_uri += "client_id=" + client_id
    login_request_uri += "&redirect_uri=" + redirect_uri
    login_request_uri += '&response_type=code'

    return redirect(login_request_uri)

def oauth(request):
    code=request.GET['code']
    print('mycode = ' +str(code))

    client_id = '9529fd434fd3250003c8cd727617a243'
    redirect_uri = "http://127.0.0.1:8000/oauth"

    access_token_request_uri = "https://kauth.kakao.com/oauth/token?grant_type=authorization_code&"

    access_token_request_uri += "client_id=" + client_id
    access_token_request_uri += "&redirect_uri=" + redirect_uri
    access_token_request_uri += "&code=" + code

    access_data = requests.get(access_token_request_uri)
    json_data = access_data.json()
    access_token = json_data['access_token']

    user_profile_uri = "https://kapi.kakao.com/v2/user/me?access_token="
    user_profile_uri += str(access_token)
    user_profile_uri_data = requests.get(user_profile_uri)
    user_json_data = user_profile_uri_data.json()


    user_nickname = user_json_data['properties']['nickname']
    
    print("aaa = " + user_nickname)

    return redirect('index')


        



def signup_create(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        user_id = request.POST.get("user_id")
        user_password = request.POST.get("user_password")
        user_password2 = request.POST.get("user_password2")
        user_info = request.POST.get("user_info")
        user_email = request.POST.get("user_email")
        user_phone = request.POST.get("user_phone")

        if user_name == "" or user_id == "" or user_password == "" or user_password2 =="" or user_info == "" or user_email == "" or user_phone == "":
            messages.info(request, "빈칸이 있음")
            return redirect('signup') ##빈 정보 있을시 회원가입페이지 그대로

        if user_password != user_password2:
            messages.info(request, "비밀번호 확인이 다릅니다.")
            return redirect('signup')

        if len(user_info) != 8:
            messages.info(request, "올바르지 못한 생년월일 형식입니다")
            return redirect('signup')

        if user_password == user_password2:

            if User.objects.filter(username=user_id).exists():
                messages.info(request,"중복된 아이디가 있어욤")
                return redirect('signup')

            else:
                user = User.objects.create_user(username=user_id, password=user_password2)
                user.is_active = True
                user.save()
                member = Member(user=user, mem_name=user_name, mem_email=user_email, mem_info=user_info, mem_phone=user_phone)
                auth.login(request, user)
                return render(request, "success.html")
    else:
        return render(request, 'index.html')

def login_try(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        user_password = request.POST['user_password']
        user = auth.authenticate(request, username=user_id, password=user_password)
        product = Product.objects
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, "일치하는 정보가 없습니다.")
            return render(request, 'login.html')

    else:
        return render(request, 'login.html')
        

def logout(request):
    auth.logout(request)
    return redirect('index')
# Create your views here.
