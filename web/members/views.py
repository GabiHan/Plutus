from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages 
from .forms import UserRegistrationForm


#Define registration here 
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('home')  # Redirect to home after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'members/register.html', {'form': form})


