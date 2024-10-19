from django import forms 
from django.contrib.auth.models import User
from members.models import Member


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label= "Set a paswword")
    #config
    class Meta:
        model = Member
        fields = ['login', 'password','firstname', 'lastname', 'age', 'birth']


