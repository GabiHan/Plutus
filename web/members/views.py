from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import UserProfile, Member, finance  # Import the custom Member model
from django.http import HttpResponse

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
        user = authenticate(request, login=login, password=password)  # Adjusted to your Member model
        if user is not None:
            auth_login(request, user)  # Use the renamed login function
            return redirect('user_profile')  # Redirect to user profile
        else:
            print("Authentication failed")
            messages.error(request, 'Invalid credentials.')  # Use messages framework for error
            return render(request, 'members/login.html', {'error': 'Invalid credentials.'})
    else:
        return render(request, 'members/login.html')  # Render login template for GET request


#define user input in his profile    
@login_required
def user_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        user_bio = request.POST.get('bio')
        tab_money = request.POST.get('money')
        tab_comment = request.POST.get('comment')
        tab_date = request.POST.get('money_date')  

        #User bio definition
        if user_bio: 
            profile.bio = user_bio 
            profile.save()  
            messages.success(request, 'Bio updated successfully!')
        else:
            messages.error(request, 'Bio cannot be empty.')  


        # Save user's entries about his wallet
        if tab_money and tab_comment and tab_date:
            finance.objects.create(
                profile=profile,
                money=tab_money,
                comment=tab_comment,
                date=tab_date
            )
            messages.success(request, 'Financial entry successfully added!')
        else:
            messages.error(request, "All financial fields must be filled.")


    financial_entries = profile.financial_entries.all()

    return render(request, 'members/index.html', {'profile': profile, 'financial_entries': financial_entries})
