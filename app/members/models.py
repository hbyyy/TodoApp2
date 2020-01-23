from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    USER_TYPE_CHOICE = (
        ('N', 'NAVER'),
        ('F', 'FACEBOOK'),
        ('D', 'DEFAULT')
    )
    name = models.CharField(max_length=20)
    type = models.CharField(choices=USER_TYPE_CHOICE, max_length=1, default='D')
