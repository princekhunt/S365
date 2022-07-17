from datetime import datetime
from http import client
from multiprocessing.connection import Client
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Active_logins, Client_accounts, Clients, Failed_login_attempts
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from S365_auth.microtools import *
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

def index(request):
    #get subdomain
    subdomain = request.META['HTTP_HOST'].split('.')[0]
    #check client
    if Clients.objects.filter(name=subdomain).exists():
        return HttpResponse(subdomain)
    else:
        return HttpResponse('Client is not active')

def auth(request):

    #get ip for production
    #ip = request.META['REMOTE_ADDR']

    #get ip for development
    r = requests.get('https://api.ipify.org')
    ip = r.text
    ip = '194.163.143.214'

    #check client
    subdomain = request.META['HTTP_HOST'].split('.')[0]
    if not Clients.objects.filter(name=subdomain).exists():
        return HttpResponse('Error Occured with Error-code : FR01')
    if not request.GET.get('ukey'):
        return HttpResponse('Forged Request Error-code: FR02')
    ukey = request.GET.get('ukey')

    #Register and auto-login and redirect
    if request.method=='POST' and request.POST.get('email') and request.POST.get('password1') and request.POST.get('password2') and request.POST.get('name'):
        name=request.POST.get('name')
        email = request.POST.get('email').lower()
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password != password2:
            return JsonResponse({
                'status':8,
                
            })
        password = make_password(password)

        #check email
        if valid_email(email) == False:
            return JsonResponse({
                'status':4,
                'error': 'Sorry, we cannot accept this email address. Please try another one.',

            })

        if not Client_accounts.objects.filter(client=Clients.objects.get(name=subdomain), email=email, password=password).exists():
            Client_accounts(name=name, email=email, password=password, client=Clients.objects.get(name=subdomain)).save()
            import random
            import string
            token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(21))
            Active_logins(client=Clients.objects.get(name=subdomain), account=Client_accounts.objects.get(email=email), ukey=ukey, token=token).save()
            url = 'http://'+subdomain+'.com:8001/auth/callback_token'
            data = {
                'ukey':ukey,
                'token':token,
                'email': email,
                'name': name
            }
            r = requests.post(url, data=data)
            
            return JsonResponse({
                'status':1,
                'location':'http://'+subdomain+'.com:8001/auth/callback?ukey='+ukey,
            })
        else:
            return JsonResponse({
                'status':0,
            })

    #Login and redirect
    if request.method=='POST' and request.POST.get('email') and request.POST.get('password'):
        email = request.POST.get('email')
        password = request.POST.get('password')

        #check login
        
        if Client_accounts.objects.filter(email=email).exists() and check_password(password, Client_accounts.objects.get(email=email).password):
            
            if Failed_login_attempts.objects.filter(account=Client_accounts.objects.get(email=email)).exists():
                send_otp(email, subdomain, ukey)
                return JsonResponse({
                    'status':6,
                    'error':"We need extra layer of authentication to identify you. We have sent you an OTP to your email. Please enter it to login.",
                })

            if check_ip(ip) > 50 or check_abuse_ip_list(ip) == True:
                send_otp(email, subdomain, ukey)
                return JsonResponse({
                    'status':5,
                    'error':"We need extra layer of authentication to identify you. We have sent you an OTP to your email. Please enter it to login.",                })
            #generate secure token
            import random
            import string
            token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(21))
            Active_logins(client=Clients.objects.get(name=subdomain), account=Client_accounts.objects.get(email=email), ukey=ukey, token=token).save()
            
            url = 'http://'+subdomain+'.com:8001/auth/callback_token?ukey='+ukey
            data = {
                'ukey':ukey,
                'token':token,
                'email': email,
                'name': Client_accounts.objects.get(email=email).name
            }
            r = requests.post(url, data=data)


            return JsonResponse({
                'status':1,
                'location':'http://'+subdomain+'.com:8001/auth/callback?ukey='+ukey,
            })
        else:
            Failed_login_attempts(count=+1, client=Clients.objects.get(name=subdomain), ip=ip, account=Client_accounts.objects.get(email=email), time=datetime.now()).save()
            return JsonResponse({
                'status':0,
            })
    if request.method == 'POST' and request.POST.get('otp'):
        ukey = request.GET.get('ukey')
        if two_factor_authentication.objects.filter(client=Clients.objects.get(name=subdomain), otp=request.POST.get('otp')).exists():
            tfa = two_factor_authentication.objects.get(ukey=ukey, client=Clients.objects.get(name=subdomain), otp=request.POST.get('otp'))
            print("Successs")
            import random
            import string
            token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(21))
            Active_logins(client=Clients.objects.get(name=subdomain), account=Client_accounts.objects.get(email=tfa.account.email), ukey=ukey, token=token).save()
                
            url = 'http://'+subdomain+'.com:8001/auth/callback_token?ukey='+ukey
            data = {
                'ukey':ukey,
                'token':token,
                'email': tfa.account.email,
                'name': tfa.account.name
            }
            r = requests.post(url, data=data)
            return JsonResponse({
                'status':6,
                'location':'http://'+subdomain+'.com:8001/auth/callback?ukey='+ukey,
            })
            
    return render(request, 'auth.html')

def check(request):
    #check client
    subdomain = request.META['HTTP_HOST'].split('.')[0]
    if not Clients.objects.filter(name=subdomain).exists():
        return JsonResponse({'status':'Forbidden',}, status=403)

    if not request.GET.get('ukey'):
        return JsonResponse({'status':'Forbidden',}, status=403)

    if request.method=='POST':
        email = request.POST.get('email')
        email = email.lower()
        if Client_accounts.objects.filter(client__name=subdomain, email=email).exists():
            return JsonResponse({'status':1})
        else:
            return JsonResponse({'status':0})

    return JsonResponse({
        'status':'Forbidden',
    }, status=403)


@csrf_exempt
def check_login(request):
    #check client
    subdomain = request.META['HTTP_HOST'].split('.')[0]
    if not Clients.objects.filter(name=subdomain).exists():
        return JsonResponse({'status':'Forbidden',}, status=403)
    
    try:
        token = request.GET.get('token')
    except:
        return JsonResponse({'status':'Forbidden'}, status=403)
    
    if Active_logins.objects.filter(token=token).exists():
        return JsonResponse({'status':True})
    return JsonResponse('Forbidden', status=403)


@csrf_exempt
def check_token(request):
    #check client
    subdomain = request.META['HTTP_HOST'].split('.')[0]
    if not Clients.objects.filter(name=subdomain).exists():
        return JsonResponse({'status':'Forbidden',}, status=403)
    
    try:
        token = request.GET.get('token')
    except:
        return JsonResponse({'status':'Forbidden'}, status=403)
    
    if Active_logins.objects.filter(token=token).exists():
        return JsonResponse(
            {'status':True,

            }
        )
    return JsonResponse('Forbidden', status=403)

@csrf_exempt
def logout(request):
    #check client
    subdomain = request.META['HTTP_HOST'].split('.')[0]
    if not Clients.objects.filter(name=subdomain).exists():
        return JsonResponse({'status':'Forbidden'}, status=403)

    if request.method == 'POST':
        print("Post rec")
        token = request.POST.get('token')
        if Active_logins.objects.filter(token=token).exists():
            Active_logins.objects.get(token=token).delete()
            return JsonResponse({'status':True})

    return JsonResponse({'status':'Forbidden'}, status=403)