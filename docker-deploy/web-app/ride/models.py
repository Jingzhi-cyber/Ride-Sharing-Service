from django.db import models
from datetime import date
from django.contrib.auth.models import User, AbstractUser

class UserEx(models.Model):
    IS_DRIVER = (
        ('false', 'false'),
        ('true', 'true'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_driver = models.CharField(max_length=10, choices=IS_DRIVER, default='false')
    
    def __str__(self):
        return self.is_driver

class Ride(models.Model):
    STATUS = (
        ('open', 'open'),
        ('confirmed', 'confirmed'),
        ('completed', 'completed'),
    )
    status = models.CharField(max_length=20, choices=STATUS, default='open')
    
    destination = models.CharField(max_length=128)
    arrival_time = models.DateTimeField()
    passenger_number = models.IntegerField()
    total_number = models.IntegerField(default=1)
    vehicle_required = models.CharField(max_length=50, blank=True)
    vehicle_type = models.CharField(max_length=50, blank=True)
    special_request = models.CharField(max_length= 100, blank=True)
    is_share = models.BooleanField(default=False)
    driver = models.ForeignKey(User, blank=True, null=True, related_name='driver', on_delete=models.CASCADE)
    sharers = models.ManyToManyField(User, blank=True, related_name='sharers')
    owner= models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    

    def __str__(self):
        return self.destination


class Sharer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Sharer')
    party_number = models.IntegerField(default=1)
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='Ride')
    

class Vehicle(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    vehicle_type = models.CharField(max_length=50)
    license_number=models.CharField(max_length=50)
    max_capacity = models.IntegerField(default=4)
    special_info = models.CharField(max_length=200, blank=True)
