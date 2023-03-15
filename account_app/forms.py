from django import forms
from account_app import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
USER =get_user_model()


class ProfileForm(forms.ModelForm):

    class Meta:
        model = models.ProfileModel
        fields = ["first_name", "last_name", "age", "gender","image","phone"]


class SignupForm(UserCreationForm):
    class Meta:
        model =USER
        fields = ["email","username"]