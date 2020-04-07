from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class DoctorProfileDB(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=10)
    profile_pic = models.CharField(max_length=500)    
    qualification = models.CharField(max_length=500)
    age = models.IntegerField()
    phone = models.CharField(max_length=20)    
    cunsultation_fee = models.IntegerField()

    def __str__(self):
        return self.user.username
class GymExpertProfileDB(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=10)
    profile_pic = models.CharField(max_length=500)           
    age = models.IntegerField()
    phone = models.CharField(max_length=20)        

    def __str__(self):
        return self.user.username
class UserProfileDB(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=10)
    profile_pic = models.CharField(max_length=500, blank=True)          
    d_o_b = models.DateTimeField(default=datetime.now,null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)    
    blood_group = models.CharField(max_length=10, blank=True)
    gender = models.CharField(max_length=10, blank=True)  

    def __str__(self):
        return self.user.username
class AdminProfileDB(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=10)
    profile_pic = models.CharField(max_length=500)           
    age = models.IntegerField()
    phone = models.CharField(max_length=20)    

    def __str__(self):
        return self.user.username
class UserMembershipDB(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joining_date = models.DateField(null=True, blank=True)
    plan = models.CharField(max_length=100)
    vallet = models.CharField(null=True,max_length=100)
    expery_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.plan