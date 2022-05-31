from django.db import models

# Create your models here.

class data(models.Model):
    name=models.CharField(max_length=1000)
    price=models.IntegerField()
    time=models.DateTimeField(auto_now_add=True)
    product = models.CharField(max_length=100)
    hash = models.CharField(max_length=1000)
    number = models.CharField(max_length=100)

class blocks_data(models.Model):
    previous_hash = models.CharField(max_length = 5000)
    current_hash = models.CharField(max_length = 5000)
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.CharField(max_length=1000)

class user_DB(models.Model):
    company = models.CharField(max_length=1000)
    username = models.CharField(max_length=100)
    
    
    