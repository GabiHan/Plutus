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
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Member, Message

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

def search_view(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Member.objects.filter(
            Q(login__icontains=query) |
            Q(firstname__icontains=query) |
            Q(lastname__icontains=query)
        )

    return render(request, 'search.html', {'results': results})
        
@login_required
@csrf_protect
def user_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':

        action = request.POST.get("action")

        # ---------------- BIO ----------------
        if action == "update_bio":
            bio = request.POST.get("bio")
            if bio:
                profile.bio = bio
                profile.save()

        # ---------------- IMAGE ----------------
        elif action == "upload_image":
            if "profile_image" in request.FILES:
                profile.profile_image = request.FILES["profile_image"]
                profile.save()
                messages.success(request, "Image uploaded!")
            else:
                messages.error(request, "No file detected.")

        # ---------------- FINANCE ----------------
        elif action == "add_money":
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
            else:
                messages.error(request, "All financial fields must be filled.")

    # ---------------- SEARCH ----------------
    query = request.GET.get('q')
    results = []

    if query:
        results = Member.objects.filter(
            Q(login__icontains=query) |
            Q(firstname__icontains=query) |
            Q(lastname__icontains=query)
        ).exclude(id=request.user.id)  # avoid showing yourself

    # ---------------- DATA ----------------
    financial_entries = profile.financial_entries.all()

    return render(request, 'members/index.html', {
        'profile': profile,
        'financial_entries': financial_entries,
        'results': results  # ✅ NEW
    })
    
def send_message(request, member_id):
    receiver = get_object_or_404(Member, id=member_id)

    if request.method == "POST":
        content = request.POST.get('content')

        if content:
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content
            )
            messages.success(request, "Message sent!")
        else:
            messages.error(request, "Empty message!")

    return redirect('search')