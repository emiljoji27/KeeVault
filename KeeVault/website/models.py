from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class PasswordModel(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True)
    login_username = models.CharField(max_length=30, blank=True)
    login_password = models.CharField(max_length=100, blank=True)
    login_url = models.CharField(max_length=30, blank=True)
    aes_key = models.CharField(max_length=30, blank=True)
    def __str__(self):
        return self.name

User._meta.get_field('email')._unique = True