from django.db import models
from django.utils import timezone
# Create your models here.
class RegisteredUser(models.Model):
    name = models.CharField(max_length=100)
    encoding = models.TextField()  # store base64 string or JSON list of floats


class Attendace(models.Model):
    name = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
