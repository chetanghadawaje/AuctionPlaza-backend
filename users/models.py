from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    username = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=10)
    email = models.EmailField(unique=True, max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
