from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
import requests

def index(request):
    product = Product.objects
    return render(request, 'index.html', {'product':product})
    
def detail(request, product_id):
    product_detail = get_object_or_404(Product, pk=product_id)
    return render(request, 'detail.html', {'i':product_detail})

def kakaopay(request):
    if request.method == "POST":
        URL = "https://kapi.kakao.com/v1/payment/ready"
        headers = {
            "Authorization" : "KakaoAK "+ "1ac98f9019dbe9545ea84d1706232e97",
            "Content-type" : "application/x-www-form-urlencoded;charset=utf-8",
        }

        params = {
            "cid":"TC0ONETIME",
            "partner_order_id":"1001",
            "partner_user_id":"퍼네이션_테스트",
            "item_name":"아이폰기부니",
            "quantity":"1",
            "total_amount":"1000",
            "tax_free_amount":"0",
            "approval_url":"http://127.0.0.1:8000/donation/pay/approval",
            "cancel_url":"http://127.0.0.1:8000/donation/pay/cancle",
            "fail_url":"http://127.0.0.1:8000/donation/pay/fail",
        }
        res = requests.post(URL, headers=headers, params=params)
       

        request.session['tid'] = res.json()['tid']
        next_url = res.json()['next_redirect_pc_url']
       
        return redirect(next_url)

    return render(request, 'index.html')

def payapproval(request):
    URL = "https://kapi.kakao.com/v1/payment/approve"
    headers = {
        "Authorization" : "KakaoAK "+ "1ac98f9019dbe9545ea84d1706232e97",
        "Content-type" : "application/x-www-form-urlencoded;charset=utf-8",
    }

    params = {
        "cid" : "TC0ONETIME",
        "tid":request.session['tid'],
        "partner_order_id":"1001",
        "partner_user_id":"퍼네이션_테스트",
        "pg_token":request.GET.get("pg_token"),
    }
    res = requests.post(URL, headers=headers, params=params)
    amount = res.json()['amount']['total']
    res = res.json()

    ##transaction 쌓아놓기
    context = {
        'res':res,
        'amount':amount,
    }

    return render(request, 'payapproval.html',context)

def paycancle(request):
    return render(request, 'paycancle.html')

def payfail(request):
    return render(request, 'payfail.html')
# Create your views here.
