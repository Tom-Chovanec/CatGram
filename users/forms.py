from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class LoginUserForm(AuthenticationForm):
    class Meta:
        fields = ["username", "password"]
        labels = {
            "username": "Username",
            "password": "Password",
        }
