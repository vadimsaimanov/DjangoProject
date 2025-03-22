from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('psychologist', 'Психолог'),
    ]
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    agreed_to_terms = models.BooleanField(default=False)  # Согласие с пользовательским соглашением
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, default='user') #роль для пользователя и психолога

    def __str__(self):
        return self.username