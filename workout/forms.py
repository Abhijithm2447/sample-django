from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from workout.models import DoctorProfileDB, UserProfileDB, UserMembershipDB


class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    def save(self, commit=True):
        user = super().save(commit=True)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user

class DoctorProfileForm(ModelForm):
    
    class Meta:
        model = DoctorProfileDB
        fields = ("group", "profile_pic", "qualification", "age", "phone", "cunsultation_fee")
class UserProfileForm(ModelForm):
    
    class Meta:
        model = UserProfileDB
        fields = "__all__"
class UserMemspForm(ModelForm):
    
    class Meta:
        model = UserMembershipDB
        fields = "__all__"