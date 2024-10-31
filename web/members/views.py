from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import UserProfile, Member  # Import the custom Member model

# Define registration here 
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Create a new Member instance
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login_view')  # Redirect to the login page after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'members/register.html', {'form': form})

def login_view(request):  # Renamed to avoid conflict
    if request.method == 'POST':
        login = request.POST.get('login')  # This should match your input field name
        password = request.POST.get('password')
        user = authenticate(request, username=login, password=password)  # Use 'username'
        
        if user is not None:
            auth_login(request, user)  # Use the renamed login function
            return redirect('user_profile')  # Redirect to user profile
        else:
            messages.error(request, 'Invalid credentials.')  # Use messages framework for error
            return render(request, 'members/login.html', {'error': 'Invalid credentials.'})
    
    return render(request, 'members/login.html')  # Render login template for GET request

@login_required
def user_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'members/index.html', {'profile': profile})
