from django.contrib import admin
from workout.models import DoctorProfileDB, UserProfileDB, AdminProfileDB, GymExpertProfileDB

admin.site.register(DoctorProfileDB)
admin.site.register(UserProfileDB)
admin.site.register(AdminProfileDB)
admin.site.register(GymExpertProfileDB)
