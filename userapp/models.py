from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='O')
    age = models.PositiveIntegerField(null=True, blank=True)
    bust = models.FloatField(null=True, blank=True)
    shoulder = models.FloatField(null=True, blank=True)
    hip = models.FloatField(null=True, blank=True)
    waist = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.username
