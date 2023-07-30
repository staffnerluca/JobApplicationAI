from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Users(AbstractUser):
    fullName = models.CharField(max_length = 50, null = True, blank = True)
    position = models.CharField(max_length = 50, null = True, blank = True)
    positionNow = models.CharField(max_length = 50, null = True, blank = True)
    companyNow = models.CharField(max_length = 50, null = True, blank = True)
    education = models.TextField(null = True, blank = True)
    skills = models.TextField(null = True, blank = True)
    experience = models.TextField(null = True, blank = True)
    achievements = models.TextField(null = True, blank = True)
    sideProjects = models.TextField(null = True, blank = True)
    requestNumber = models.PositiveIntegerField(null = True, blank = True)
