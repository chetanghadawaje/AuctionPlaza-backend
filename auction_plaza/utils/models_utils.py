from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)


class BaseModelLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)