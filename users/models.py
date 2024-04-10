from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    username = models.CharField(max_length=50, null=True, blank=True)
    mobile_number = models.CharField(max_length=10)
    email = models.EmailField(unique=True, max_length=50, db_index=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
