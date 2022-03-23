from sqlite3 import Timestamp
from unicodedata import category
from unittest.util import _MAX_LENGTH
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

class manuData(models.Model):
    display_uid = models.CharField(max_length=4)
    # blank= False
    ram_uid = models.CharField(max_length=4)
    hdd_uid = models.CharField(max_length=4)
    ssd_uid = models.CharField(max_length=4)
    processor_uid = models.CharField(max_length=4)
    graphics_uid = models.CharField(max_length=4)
    battery_uid = models.CharField(max_length=4)

class save_uid(models.Model):
    username = models.CharField(max_length=100)
    uid_list = models.JSONField()
    category = models.CharField(max_length=100)

class transactions(models.Model):
    sender_username = models.CharField(max_length=100)
    sender_category = models.CharField(max_length=100)
    uid = models.JSONField()
    receiver_username = models.CharField(max_length=100)
    receiver_category = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)