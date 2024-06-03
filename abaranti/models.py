from django.db import models
from django.contrib.auth.models import AbstractUser

class Employee(AbstractUser):
    class Role(models.IntegerChoices):
        RECEPTION = 0, '受付'
        DOCTOR = 1, '医師'

    # empidをusernameとして使う
    username = models.CharField(max_length=8, primary_key=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)  # ハッシュ化されたパスワードを保存
    role = models.IntegerField(choices=Role.choices)
