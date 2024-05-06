from django.contrib.auth.forms import UserCreationForm #Django User Creation Form
from django import forms
from django.contrib.auth.models import User #User class in Django

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        #fields=['username','email','password']


