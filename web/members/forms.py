from django import forms
from .models import Member

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter a secure password'})
    )

    class Meta:
        model = Member
        fields = ['login', 'firstname', 'age', 'lastname', 'password']

        widgets = {
            'login': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'firstname': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'lastname': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Your Age'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash password
        if commit:
            user.save()
        return user
