from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Clients)
admin.site.register(Client_accounts)
admin.site.register(Active_logins)