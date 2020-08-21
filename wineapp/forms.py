from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *


class CreateUserForm(UserCreationForm):
    # replica of the default UserCreationForm, but customize the fields
    class Meta:
        model = User
        fields = ['username','email','password1','password2']