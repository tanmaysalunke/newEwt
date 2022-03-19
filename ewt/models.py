from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

CATEGORY = (
    ('Manufacturer', 'Manufacturer'),
    ('Refurbisher', 'Refurbisher'),
    ('Recycler', 'Recycler')
)

class CustomUser(AbstractUser):
    company_name = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    category = models.CharField(choices=CATEGORY, max_length=50, default='Manufacturer')