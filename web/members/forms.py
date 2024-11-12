from django import forms
from .models import Member, MemberManager, UserProfile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    

    class Meta:
        model = Member
        fields = ['login', 'firstname','age', 'lastname', 'password']  # Add all necessary fields


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Ensure password is hashed
        if commit:
            user.save()
        return user