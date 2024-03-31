from django.db import models
from django.contrib.auth.models import AbstractUser

class UserManage(AbstractUser):
    username = models.CharField(max_length=12, unique=True)
    is_technician = models.BooleanField(default=False)
    is_staff_member = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)