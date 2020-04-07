from django.shortcuts import render
from django.views.generic import View
from workout.mixins import HttpresponseMixin, SerializerMixin, is_json
from workout.models import DoctorProfileDB
from workout.forms import ExtendedUserCreationForm, DoctorProfileForm, UserProfileForm, UserMemspForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
# model
from workout.models import UserProfileDB, DoctorProfileDB, GymExpertProfileDB, AdminProfileDB, UserMembershipDB

# common
import base64
from PIL import Image
from io import BytesIO
import numpy as np
import json
import os

import pdb

path_profile_pic = os.path.join("static", "user_profile_pic")

@method_decorator(csrf_exempt, name='dispatch')
class WorkoutView(HttpresponseMixin, SerializerMixin, View):
    def get(self, request, *args, **kwargs):
        if User.groups.filter(name='group1') == True:
            print("This is a physician")
        json_data = json.dumps({'message': "Message from server"})
        return self.render_to_http_response(json_data, status=200)
    def post(self, request, *args, **kwargs):
        json_data = json.dumps({'message': "Message from server"})
        return self.render_to_http_response(json_data, status=200)
#------------------------------------------------------------------------------------
#                                      REST API                                     #
#____________________________________________________________________________________
# User registration api
#____________________________________________________________________________________
# url: user_reg/
# input
# =====
# {

# }
#____________________________________________________________________________________
@method_decorator(csrf_exempt, name='dispatch')
class UserRegistration(HttpresponseMixin, SerializerMixin, View):
    def get(self, request, *args, **kwargs):
        form = ExtendedUserCreationForm()
        # profile_form = DoctorProfileForm()
        context = {'form': form,
                    # 'profile_form':profile_form
                }
        return render(request, "index.html", context)
    def post(self, request, *args, **kwargs):
        result = {}
        error = []
        messsage = []
        flag = True
        data = request.body  
        # pdb.set_trace()              
        if is_json(data):
            data = json.loads(data)
            if "username" in data:
                username = data["username"]
            else:
                flag = False                
                error.append("username is not given")
            if "email" in data:
                email = data["email"]
            else:
                flag = False                
                error.append("email is not given")
            if "first_name" in data:
                first_name = data["first_name"]
            else:
                flag = False                
                error.append("first_name is not given")
            if "last_name" in data:
                last_name = data["last_name"]
            else:
                flag = False                
                error.append("last_name is not given")
            if "password1" in data:
                password1 = data["password1"]
            else:
                flag = False                
                error.append("password1 is not given")
            if "password2" in data:
                password2 = data["password2"]
            else:
                flag = False                
                error.append("password2 is not given")
        else:
            error.append("Invalid json data")
            status = 400
            flag = False
        if flag: 
            form_data = {
                "username" : username,
                "email" : email,
                "first_name" : first_name,
                "last_name" : last_name,
                "password1" : password1,
                "password2" : password2,
            }   
            
            form = ExtendedUserCreationForm(form_data)        

            if form.is_valid():            
                user = form.save()
                print(user, user.id)
                result['user_creation'] = True 
                result['user_id'] = user.id 
                status = 200                      
            if form.errors:   
                status = 400        
                error.append(form.errors)
        else:
            status = 400
        json_data = json.dumps({'result':result, 'error':error, 'message': messsage})
        return self.render_to_http_response(json_data, status=status)
#____________________________________________________________________________________
# Doctor registration api
#____________________________________________________________________________________
# url: physician_reg/
# input
# =====
# {
    # 'username':"physician4",
    # "password" : "initial#024",
    # 'group':'physicians',
    # 'profile_pic': encoded_string,
    # 'qualification': 'MBBS',
    # 'age': 20,
    # 'phone': 9447838962,
    # 'cunsultation_fee': 20,
# }
#____________________________________________________________________________________
@method_decorator(csrf_exempt, name='dispatch')
class PhysicianRegistration(HttpresponseMixin, SerializerMixin, View):
    def get(self, request, *args, **kwargs):        
        profile_form = DoctorProfileForm()
        context = {
                    'profile_form':profile_form
                }
        return render(request, "index.html", context)
    def post(self, request, *args, **kwargs):
        result = {}
        error = []
        messsage = []
          
        flag = True
               
        
        data = request.POST

        if "username" in data:
            username = data["username"]
        else:
            flag = False                
            error.append("username is not given")
        if "password" in data:
            password = data["password"]
        else:
            flag = False                
            error.append("password is not given")
        if "group" in data:
            group = data["group"]
        else:
            flag = False                
            error.append("group is not given")
        if "profile_pic" in data:
            profile_pic = data["profile_pic"]
        else:
            flag = False                
            error.append("profile_pic is not given")
        if "qualification" in data:
            qualification = data["qualification"]
        else:
            flag = False                
            error.append("qualification is not given")
        if "age" in data:
            age = data["age"]
        else:
            flag = False                
            error.append("age is not given")
        if "phone" in data:
            phone = data["phone"]
        else:
            flag = False                
            error.append("phone is not given")
        if "cunsultation_fee" in data:
            cunsultation_fee = data["cunsultation_fee"]
        else:
            flag = False                
            error.append("cunsultation_fee is not given")
        
        if flag:             
            try:
                profile_im = Image.open(BytesIO(base64.b64decode(base64.b64decode(profile_pic))))
                path_image = os.path.join(path_profile_pic, username+".png")                
            except:
                error.append("Cant decode image. Base64 encoding error. Please encode your image in two times.")
            form_data = {                
                "group" : group,
                "profile_pic": path_image,
                "qualification" : qualification,
                "age" : age,
                "phone" : phone,
                "cunsultation_fee" : cunsultation_fee,
            }      
                
            profile_form = DoctorProfileForm(form_data)
            
            if profile_form.is_valid():               
                status = 200
                profile = profile_form.save(commit=False)

                user = authenticate(username= username, password=password)
                user = User.objects.get(id=user.id)
                profile.user = user
                try:
                    profile.save()
                    result['user_profile_creation'] = True
                    try:
                        profile_im.save(path_image, 'PNG')
                    except:
                        error.append("image is not saved")
                except:
                    status = 400
                    error.append("User profile is already created in this user. Please do update user profile.")
                    result['user_profile_creation'] = False
            else:
                status = 402                       
            if profile_form.errors:   
                status = 402         
                error.append(profile_form.errors)
        else:
            status = 400
        json_data = json.dumps({'result':result, 'error':error, 'message': messsage})
        return self.render_to_http_response(json_data, status=status)
#____________________________________________________________________________________
# Login User
#____________________________________________________________________________________
# url : login_user/
#____________________________________________________________________________________
@method_decorator(csrf_exempt, name='dispatch')
class LoginUser(HttpresponseMixin, SerializerMixin, View):
    def get(self, request, *args, **kwargs):
        form = ExtendedUserCreationForm()
        # profile_form = DoctorProfileForm()
        context = {'form': form,
                    # 'profile_form':profile_form
                }
        return render(request, "index.html", context)
    def post(self, request, *args, **kwargs):
        result = {}
        error = []
        messsage = []
        flag = True
        data = request.body                
        if is_json(data):
            data = json.loads(data)
            if "username" in data:
                username = data["username"]
            else:
                flag = False                
                error.append("username is not given")            
            if "password" in data:
                password = data["password"]
            else:
                flag = False                
                error.append("password is not given")            
        else:
            error.append("Invalid json data")
            status = 400
            flag = False
        if flag: 
            status = 200
            user = authenticate(username= username, password=password)
            flag_user = False
            if UserProfileDB.objects.filter(user = user).count() > 0:
                obj_userprofile = UserProfileDB.objects.filter(user = user)
                for user_p in obj_userprofile:
                    result["group"] = user_p.group 
                    result["f_name"] = user.first_name
                    result["l_name"] = user.last_name 
                    flag_user = True              
                
            if AdminProfileDB.objects.filter(user = user).count() > 0:
                obj_userprofile = AdminProfileDB.objects.filter(user = user)
                for user_p in obj_userprofile:
                    result["group"] = user_p.group 
                    result["f_name"] = user.first_name
                    result["l_name"] = user.last_name
                    flag_user = True               
                
            if GymExpertProfileDB.objects.filter(user = user).count() > 0:
                obj_userprofile = GymExpertProfileDB.objects.filter(user = user)
                for user_p in obj_userprofile:
                    result["group"] = user_p.group 
                    result["f_name"] = user.first_name
                    result["l_name"] = user.last_name
                    flag_user = True               
                
            if DoctorProfileDB.objects.filter(user = user).count() > 0:
                obj_userprofile = DoctorProfileDB.objects.filter(user = user)
                for user_p in obj_userprofile:
                    result["group"] = user_p.group  
                    result["f_name"] = user.first_name
                    result["l_name"] = user.last_name
                    flag_user = True
            if not flag_user:
                error.append("invalid user")
                
        else:
            status = 400
        json_data = json.dumps({'result':result, 'error':error, 'message': messsage})        
        return self.render_to_http_response(json_data, status=status)
#____________________________________________________________________________________
# User Profile api
#____________________________________________________________________________________
# url: user_prof_reg/
# input
# =====
# {
    # "user_id" : 16,
    # "prof_pic" : "",
    # "d_o_b" : "",
    # "phone" : "",
    # "blood_group" : "",
    # "gender" : ""
# }
#____________________________________________________________________________________
@method_decorator(csrf_exempt, name='dispatch')
class UserProfReg(HttpresponseMixin, SerializerMixin, View):
    def get(self, request, *args, **kwargs):        
        profile_form = DoctorProfileForm()
        context = {
                    'profile_form':profile_form
                }
        return render(request, "index.html", context)
    def post(self, request, *args, **kwargs):
        result = {}
        error = []
        messsage = []          
        flag = True                       
        data = request.body        
        if is_json(data):
            data = json.loads(data)
            if "user_id" in data:
                user_id = int(data["user_id"])
            else:
                flag = False                
                error.append("user_id is not given")
            if "profile_pic" in data and data["profile_pic"] != "":
                profile_pic = data["profile_pic"]
                profile_pic_f = True
            else:
                profile_pic_f = False 
                profile_pic = " "                          
                error.append("profile_pic is not given")
            if "d_o_b" in data and data["d_o_b"] != "":
                d_o_b = data["d_o_b"]
            else: 
                d_o_b = ''                        
                error.append("d_o_b is not given")
            if "phone" in data and data["phone"] != "":
                phone = data["phone"]
            else: 
                phone = " "                          
                error.append("phone is not given")
            if "blood_group" in data and data["blood_group"] != "":
                blood_group = data["blood_group"]
            else:  
                blood_group = ' '                         
                error.append("blood_group is not given")
            if "gender" in data and data["gender"] != "":
                gender = data["gender"]
            else:
                gender = ' '            
                error.append("gender is not given")  
        else:
            error.append("Invalid json")
            status = 400
            
        if flag:
            if profile_pic_f:             
                try:
                    profile_im = Image.open(BytesIO(base64.b64decode(base64.b64decode(profile_pic))))
                    path_image = os.path.join(path_profile_pic, str(user_id)+".png")                
                except:
                    error.append("Cant decode image. Base64 encoding error. Please encode your image in two times.")
            
            user = User.objects.get(id=user_id)            
            form_data = {                
                "user" : user,
                "group": "user",
                "profile_pic" : profile_pic,
                "d_o_b" : d_o_b,
                "phone" : phone,
                "blood_group" : blood_group,
                "gender" : gender,
            }      
                
            profile_form = UserProfileForm(form_data)
            
            if profile_form.is_valid():               
                status = 200
                profile = profile_form.save()

                if profile:
                    result['user_profile_creation'] = True
                else:
                    result['user_profile_creation'] = False
            else:
                status = 400                       
            if profile_form.errors:   
                status = 400        
                error.append(profile_form.errors)
        else:            
            status = 400
        json_data = json.dumps({'result':result, 'error':error, 'message': messsage})
        return self.render_to_http_response(json_data, status=status)
#____________________________________________________________________________________
#____________________________________________________________________________________
# User Membership API
#____________________________________________________________________________________
# url: user_memsp_reg/
# input
# =====
# {
    # "user_id" : 32,
    # "joining_date" : "2020-02-20",
    # "plan" : "premium",
    # "vallet" : "200",
    # "expery_date" : "2020-08-20",
# }
#____________________________________________________________________________________
@method_decorator(csrf_exempt, name='dispatch')
class UserMemSpReg(HttpresponseMixin, SerializerMixin, View):
    def get(self, request, *args, **kwargs):        
        profile_form = DoctorProfileForm()
        context = {
                    'profile_form':profile_form
                }
        return render(request, "index.html", context)
    def post(self, request, *args, **kwargs):
        result = {}
        error = []
        messsage = []          
        flag = True                       
        data = request.body        
        if is_json(data):
            data = json.loads(data)
            if "user_id" in data:
                user_id = int(data["user_id"])
            else:
                flag = False                
                error.append("user_id is not given")
            if "joining_date" in data and data["joining_date"] != "":
                joining_date = data["joining_date"]                
            else:
                flag = False                                         
                error.append("joining_date is not given")
            if "plan" in data and data["plan"] != "":
                plan = data["plan"]
            else:  
                flag = False                                       
                error.append("plan is not given")
            if "vallet" in data and data["vallet"] != "":
                vallet = data["vallet"]
            else:  
                flag = False                                         
                error.append("vallet is not given")
            if "expery_date" in data and data["expery_date"] != "":
                expery_date = data["expery_date"]
            else: 
                flag = False                                           
                error.append("expery_date is not given")             
        else:
            flag = False
            error.append("Invalid json")
            status = 400
            
        if flag:                        
            user = User.objects.get(id=user_id) 
            print(user)           
            form_data = {                
                "user" : user,
                "joining_date": joining_date,
                "plan" : plan,
                "vallet" : vallet,
                "expery_date" : expery_date,
            }      
                
            profile_form = UserMemspForm(form_data)
            
            if profile_form.is_valid():               
                status = 200
                profile = profile_form.save()

                if profile:
                    result['memsp_creation'] = True
                else:
                    result['memsp_creation'] = False
            else:
                status = 400                       
            if profile_form.errors:   
                status = 400        
                error.append(profile_form.errors)
        else:            
            status = 400
        json_data = json.dumps({'result':result, 'error':error, 'message': messsage})
        return self.render_to_http_response(json_data, status=status)
#____________________________________________________________________________________
#____________________________________________________________________________________
#____________________________________________________________________________________
# List Gym Members
#____________________________________________________________________________________
# url: list_gym_members/
# input
# =====
# {
    # "user_id" : 32,
    # "joining_date" : "2020-02-20",
    # "plan" : "premium",
    # "vallet" : "200",
    # "expery_date" : "2020-08-20",
# }
#____________________________________________________________________________________
@method_decorator(csrf_exempt, name='dispatch')
class ListGymMembers(HttpresponseMixin, SerializerMixin, View):
    def get(self, request, *args, **kwargs):        
        profile_form = DoctorProfileForm()
        context = {
                    'profile_form':profile_form
                }
        return render(request, "index.html", context)
    def post(self, request, *args, **kwargs):
        result = {}
        error = []
        messsage = []          
        flag = True                               
            
        if flag:  
            status = 200          
            # pdb.set_trace()
            obj_user_msmsp = UserMembershipDB.objects.order_by('expery_date') 
            list_user = []
            for user in obj_user_msmsp:
                tmp = {
                    "user_id" : user.user.id,
                    'user' : user.user.first_name +" " + user.user.last_name,
                    'joining_date' : user.joining_date.strftime("%d %b, %Y"),
                    'plan' : user.plan,
                    'vallet' : user.vallet,
                    'expery_date' : user.expery_date.strftime("%d %b, %Y")
                }
                list_user.append(tmp)
                
            result['list_memsp'] = list_user                                             
        else:            
            status = 400
        json_data = json.dumps({'result':result, 'error':error, 'message': messsage})
        return self.render_to_http_response(json_data, status=status)
#____________________________________________________________________________________