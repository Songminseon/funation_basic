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


# class KaKaoLoginView(View):
#     def get(self, request):
#         app_key = '9529fd434fd3250003c8cd727617a243'

#         kakao_access_code = request.GET.get('code', None)

#         url = 'http://kauth.kakao.com/oauth/token'

#         headers = {'Content-type':'application/x-www-form-urlencoded; charset=utf-8'}

#         body = {'grant_type' : 'authorization_code', 'client_id':app_key, 'redirect_uri':'http://localhost:8000', 'code':kakao_access_code}

#         kakao_response = requests.post(url, headers=headers, data=body)
#         return HttpResponse(f'{kakao_response.text}')

# def kakao_signup(request):
#     app_key = '9529fd434fd3250003c8cd727617a243'
#     request_url = "https://kauth.kakao.com/oauth/authorize?client_id=" + app_key + "&redirect_uri=http://127.0.0.1:8000&response_type=code"
#     headers = {'Content-type':'application/x-www-form-urlencoded; charset=utf-8'}
#     kakao_access_code = request.GET.get('code',None)
#     body = {'grant_type' : 'authorization_code', 'client_id':app_key, 'redirect_uri':'http://localhost:8000', 'code':kakao_access_code}
#     kakao_response=requests.post(request_url, headers=headers, data=body)
#     information = kakao_response
#     print(information)
#     print(user_token)
#     return redirect(request_url)


def kakao_signup(request):
    app_key = '9529fd434fd3250003c8cd727617a243'
    redirect_uri = 'http://127.0.0.1:8000'
    access_token = f"https://kauth.kakao.com/oauth/authorize?client_id={app_key}&redirect_uri={redirect_uri}&response_type=code"
    my_token = requests.get(access_token)

    # url = 'https://kauth.kakao.com/oauth/token'
    # kakao_access_code = request.GET.get('code',None)
    # headers = {'Content-type':'application/x-www-form-urlencoded; charset=utf-8'}
    # body = {'grant_type' : 'authorization_code', 'client_id':app_key, 'redirect_uri':'http://localhost:8000', 'code':kakao_access_code}
    
    # kakao_response = requests.post(url, headers=headers, data=body)
    # return HttpResponse(f'{kakao_response.text}')
    print(my_token.json())
    return redirect(access_token)

class KakaoSignInView(View):
    def get(self, request):
        client_id = '9529fd434fd3250003c8cd727617a243'
        redirect_uri = "http://127.0.0.1:8000"
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        )
        
class KakaoSignInCallbackView(View):
    def get(self, request):
        try:
            code = request.GET.get("code")
            client_id = '9529fd434fd3250003c8cd727617a243'
            redirect_uri = "http://127.0.0.1:8000"

            token_request = requests.get(
                f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
            )

            token_json = token_request.json()
            
            error = token_json.get("error",None)

            if error is not None :
                return JsonResponse({"message": "INVALID_CODE"}, status = 400)

            access_token = token_json.get("access_token")

            #------get kakaotalk profile info------#

            profile_request = requests.get(
                "https://kapi.kakao.com/v2/user/me", headers={"Authorization" : f"Bearer {access_token}"},
            )
            profile_json = profile_request.json()

            kakao_account = profile_json.get("kakao_account")
            email = kakao_account.get("email", None)
            kakao_id = profile_json.get("id")

        except KeyError:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status = 400)

        except access_token.DoesNotExist:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status = 400)
           
        if Account.objects.filter(kakao_id = kakao_id).exists():
            user = Account.objects.get(kakao_id = kakao_id)
            token = jwt.encode({"email" : email}, SECRET_KEY, algorithm = "HS256")
            token = token.decode("utf-8")

            return JsonResponse({"token" : token}, status=200)

        else :
            Account(
                kakao_id = kakao_id,
                email    = email,
            ).save()

            token = jwt.encode({"email" : email}, SECRET_KEY, algorithm = "HS256")
            token = token.decode("utf-8")

            return JsonResponse({"token" : token}, status = 200)


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
