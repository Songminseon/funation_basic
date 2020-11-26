"""funation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
import main.views
import member.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main.views.index, name="index"),
    path('signup/', member.views.signup, name="signup"),
    path('login/', member.views.login, name="login"),
    path('signup/create/', member.views.signup_create, name="signup_create"),
    path('signup/create/success', member.views.success, name="success"),
    path('accounts/', include('allauth.urls')),
    path('login/login_try/', member.views.login_try, name="login_try"),
    path('login/logout/', member.views.logout, name="logout"),
    path('donation/<int:product_id>/', main.views.detail, name="detail"),
    path('donation/pay/', main.views.kakaopay, name="kakaopay"),
    path('donation/pay/approval/', main.views.payapproval, name="payapproval"),
    path('donation/pay/cancle/', main.views.paycancle, name="paycancle"),
    path('donation/pay/fail/', main.views.payfail, name="payfail"),
    path('signup/kakaoSignup', member.views.kakao_signup, name="kakao_signup"),
    path('oauth/', member.views.oauth, name="oauth"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
