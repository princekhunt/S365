import requests
import json
from django.core.mail import EmailMessage
from datetime import datetime
from S365_auth.models import Client_accounts
from S365_auth.models import Clients
from S365_auth.models import two_factor_authentication


def check_ip(ip):
    url = 'https://api.abuseipdb.com/api/v2/check'
    querystring = {
    'ipAddress': ip,
    'maxAgeInDays': '30'
    }

    headers = {
        'Accept': 'application/json',
        'Key': '7082b591404343e42f22d603504aaf0d63f27bbca1a84df0891230740494bd7c8596680d42800cda'
    }

    response = requests.request(method='GET', url=url, headers=headers, params=querystring)
    print(int(response.json()['data']['abuseConfidenceScore']))
    return int(response.json()['data']['abuseConfidenceScore'])

def check_abuse_ip_list(ip):
    url = 'https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt'
    response = requests.get(url)
    list = response.text.split('\n')
    if ip in list:
        print("True")
        return True
    else:
        print("False")
        return False

def valid_email(email):
    r = "https://isitarealemail.com/api/email/validate?email="+email
    head = {
    'Authorization': "bearer 4a68e7f3-f13b-43df-a7a0-09525c76f5df"
    }
    r = requests.get(r, headers=head)
    status = r.json()['status']
    if status == 'valid':
        return True
    return False

def send_otp(email, client, ukey):
    email = email.lower()
    #generate 6 digit otp
    import random
    import string
    otp = ''.join(random.choice(string.digits) for _ in range(6))
    #send otp to email
    email_message = EmailMessage(
        subject='S365 OTP',
        body='Your OTP is: '+otp,
        from_email='S365 Secure Login<S365.temp@princekhunt.com>',
        to=[email]

    )
    email_message.send()
    #save otp to db
    if two_factor_authentication.objects.filter(ukey=ukey, client=Clients.objects.get(name=client), account=Client_accounts.objects.get(email=email)).exists():
        two_factor_authentication.objects.filter(ukey=ukey, client=Clients.objects.get(name=client), account=Client_accounts.objects.get(email=email)).update(otp=otp)
    else:
        two_factor_authentication(ukey=ukey, client=Clients.objects.get(name=client), account=Client_accounts.objects.get(email=email), otp=str(otp), time=datetime.now()).save()
    return True