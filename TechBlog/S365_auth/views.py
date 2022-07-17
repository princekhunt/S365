from urllib import response
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from S365_auth.models import authentication_request, authentication_response
import requests
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def index(request):
    if request.COOKIES.get('token') is not None:
        #decode base64 token
        import base64
        token = base64.b64decode(request.COOKIES.get('token')).decode('utf-8')
        print(token)
        token = authentication_response.objects.get(token=token)
        url = 'http://tech-blog.S365.com:8000/auth/check_token?token='+token.token
        response = requests.get(url)
        if response.json()['status'] == True:
            #authenticated
            name = authentication_response.objects.get(token=token.token).name
            email = authentication_response.objects.get(token=token.token).email
            return render(request, 'index.html', {'name': name, 'email': email})
        else:
            #not authenticated
            return render(request, 'index.html')
    return render(request, 'index.html')

def verify_me(request):
    #generate ukey
    import random
    import string
    ukey = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(17))

    #set cookie
    response = render(request, 'verify-me.html', {'ukey': ukey}, content_type='text/html', status=302)
    response.set_cookie('ukey', ukey)
    return response

def router(request):
    ukey = request.COOKIES.get('ukey')
    print("redirecting with ukey "+ukey)
    #Save ukey in db
    import datetime
    import time
    authentication_request(ukey=ukey, timestamp=datetime.datetime.now()).save()
    return HttpResponseRedirect('http://tech-blog.S365.com:8000/auth?ukey='+ukey, status=302)

def callback(request):
    ukey = request.GET.get('ukey')

    #Check Login
    if authentication_response.objects.filter(ukey=ukey).exists():
        user = authentication_response.objects.get(ukey=ukey)
        name = user.name
        email = user.email
        token = user.token

        print(name)
        print("\n")
        print(email)
        print("\n")
        print(email)
        print("\n")

        #check login
        url = 'http://tech-blog.S365.com:8000/auth/check_login?token='+token
        response = requests.get(url)
        print(response.json())
        if not response.json()['status'] == True:
            return HttpResponse("Forged Request")


        #Save response in db
        response = HttpResponseRedirect('../', status=302)
        #base64 encode token
        import base64
        token = base64.b64encode(token.encode('utf-8')).decode('utf-8')
        response.set_cookie('token', token)
        return response
    else:
        return HttpResponse("Forged Request (ukey does not exists)")

    return HttpResponse("")

@csrf_exempt
def callback_token(request):
    if request.method == 'POST':
        ukey = request.POST.get('ukey')
        token = request.POST.get('token')
        name = request.POST.get('name')
        email = request.POST.get('email')
        print("Request received")
        #Save response in db
        if authentication_response.objects.filter(ukey=ukey).exists():
            authentication_response.objects.filter(ukey=ukey).update(token=token, name=name, email=email)
        else:
            authentication_response(ukey=ukey, token=token, name=name, email=email).save()
        return HttpResponse('hola')

def logout(request):
    url = 'http://tech-blog.S365.com:8000/auth/logout'
    data = {
        'token': request.COOKIES.get('token'),
        'action':'logout'
    }
    response = requests.post(url, data=data)
    #delete cookie
    response = HttpResponseRedirect('../', status=302)
    response.delete_cookie('token')
    response.delete_cookie('ukey')
    return response