from django.db import models

# Create your models here.


class authentication_request(models.Model):
    ukey = models.CharField(max_length=17)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.ukey

class authentication_response(models.Model):
    ukey = models.CharField(max_length=17)
    token = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.ukey