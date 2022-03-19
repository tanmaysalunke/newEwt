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

class manu_data(models.Model):
    display_uid = models.IntegerField(max_length=4)
    ram_uid = models.IntegerField(max_length=4)
    hdd_uid = models.IntegerField(max_length=4)
    ssd_uid = models.IntegerField(max_length=4)
    processor_uid = models.IntegerField(max_length=4)
    graphics_uid = models.IntegerField(max_length=4)
    battery_uid = models.IntegerField(max_length=4)