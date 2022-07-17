from http import client
from itertools import count
from django.db import models

# Create your models here.

class Clients(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

class Client_accounts(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    email = models.EmailField(max_length=1024)
    password = models.CharField(max_length=2048)

    def __str__(self):
        return self.email
    class Meta:
        verbose_name = 'Client Account'
        verbose_name_plural = 'Client Accounts'

class Active_logins(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    account = models.ForeignKey(Client_accounts, on_delete=models.CASCADE)
    ukey = models.CharField(max_length=1024)
    token = models.CharField(max_length=1024)

    def __str__(self):
        return self.ukey
    class Meta:
        verbose_name = 'Active Login'
        verbose_name_plural = 'Active Logins'

class Failed_login_attempts(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    account = models.ForeignKey(Client_accounts, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
    count = models.IntegerField(default=0)
    time = models.DateTimeField()


    def __str__(self):
        return self.ip
    class Meta:
        verbose_name = 'Failed Login Attempt'
        verbose_name_plural = 'Failed Login Attempts'

class two_factor_authentication(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    account = models.ForeignKey(Client_accounts, on_delete=models.CASCADE)
    ukey = models.CharField(max_length=1024)
    otp = models.CharField(max_length=6)
    time = models.DateTimeField()

    def __str__(self):
        return self.otp
    class Meta:
        verbose_name = 'Two Factor Authentication'
        verbose_name_plural = 'Two Factor Authentication'