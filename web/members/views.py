from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Member, finance  # Import the custom Member model
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from django.shortcuts import redirect

from django.views import View

from .forms import UserRegistrationForm


# Define registration here 
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login_view')
        else:
            messages.error(request, 'Please fill in all required fields correctly.')
    else:
        form = UserRegistrationForm()

    return render(request, 'members/register.html', {'form': form})
    
def login_view(request):  
    if request.method == 'POST':
        login = request.POST.get('login')  
        password = request.POST.get('password')
        user = authenticate(request, login=login, password=password) 
        if user is not None:
            auth_login(request, user) 
            return redirect('user_profile')  
        else:
            print("Authentication failed")
            messages.error(request, 'Invalid credentials.')  
            return render(request, 'members/login.html', {'error': 'Invalid credentials.'})
    else:
        return render(request, 'members/login.html')  

#Not functional yet, will be added in future updates
def change_pass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data= request.POST)
        if form.is_valid():
            form.save()
            update_session_auth(request, form.user)
        else :
            return render(request, 'members/login.html')

def logout_view(request):
    logout(request)
    return redirect('login_view') 
        
@login_required
@csrf_protect
def user_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':

        action = request.POST.get("action")

        if action == "update_bio":
            bio = request.POST.get("bio")
            if bio:
                profile.bio = bio
                profile.save()

        elif action == "upload_image":
            if "profile_image" in request.FILES:
                profile.profile_image = request.FILES["profile_image"]
                profile.save()

        # ---------------- FINANCE ----------------
        tab_money = request.POST.get('money')
        tab_comment = request.POST.get('comment')
        tab_date = request.POST.get('money_date')

        if tab_money and tab_comment and tab_date:
            finance.objects.create(
                profile=profile,
                money=tab_money,
                comment=tab_comment,
                date=tab_date
            )
            messages.success(request, 'Financial entry added!')
        elif any([tab_money, tab_comment, tab_date]):
            messages.error(request, "All financial fields must be filled.")

    financial_entries = profile.financial_entries.all()

    return render(request, 'members/index.html', {
        'profile': profile,
        'financial_entries': financial_entries
    })