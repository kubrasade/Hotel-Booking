from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import BaseModel

class CustomUser(BaseModel,AbstractUser):
    is_client = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)

    class Meta:
        verbose_name= "User"
        verbose_name_plural= "Users"
        
    def __str__(self):
        return self.username
    