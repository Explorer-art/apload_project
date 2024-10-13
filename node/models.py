import time
from django.db import models
from .config import *

class User(models.Model):
	ip = models.CharField(max_length=15)
	uploads = models.IntegerField(default=0)
	uploaded = models.IntegerField(default=0)
	expire = models.IntegerField(default=time.time() + EXPIRE_CLEAR)
	enable = models.BooleanField(default=True)