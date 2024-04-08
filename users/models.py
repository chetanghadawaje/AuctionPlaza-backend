from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def create_user(self, email, password, mobile_number):
        user = self.create_user(email, password)
        user.profile_picture = mobile_number
        user.save()
        return user


class User(AbstractUser):
    username = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=10)