from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    last_name = forms.CharField(max_length=5)
    first_name = forms.CharField(max_length=5)
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "last_name", "first_name", "email")
