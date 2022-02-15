from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(max_length=500,blank=True)
    block_list = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True)


class Message(models.Model):
    text = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now=True)

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='users')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING , related_name='receivers')

    def __str__(self):
        return self.sender.username + "'s Message"
