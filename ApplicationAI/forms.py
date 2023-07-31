from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users


class fRegister(UserCreationForm):
    class Meta:
        model = Users
        fields = ["username", "password"]
