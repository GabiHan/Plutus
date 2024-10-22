from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate


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

def login(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, login=login, password=password)
        if user is not None :
            login(request, user)
            return redirect('home.ht')
        else:
            return render(request, 'members/login.html', {'error': 'Invalid credentials.'})
    else:
        return render(request, 'members/login.html')

