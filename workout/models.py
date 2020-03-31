from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class DoctorProfileDB(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=10)
    profile_pic = models.CharField(max_length=500)    
    qualification = models.CharField(max_length=500)
    age = models.IntegerField()
    phone = models.IntegerField()
    cunsultation_fee = models.IntegerField()

    def __str__(self):
        return self.user.username
class GymExpertProfileDB(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=10)
    profile_pic = models.CharField(max_length=500)           
    age = models.IntegerField()
    phone = models.IntegerField()    

    def __str__(self):
        return self.user.username
class UserProfileDB(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=10)
    profile_pic = models.CharField(max_length=500)          
    d_o_b = models.DateTimeField(default=datetime.now, blank=True)
    phone = models.IntegerField()  
    blood_group = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)  

    def __str__(self):
        return self.user.username
class AdminProfileDB(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=10)
    profile_pic = models.CharField(max_length=500)           
    age = models.IntegerField()
    phone = models.IntegerField()    

    def __str__(self):
        return self.user.username
