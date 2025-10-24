from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings
import requests

def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('accounts:home')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'accounts/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone = form.cleaned_data['phone']
            
            # This line triggers the post_save signal!
            user = User.objects.create_user(username=username, email=email, password=password)
            
            
            #   # Save phone number
            user.profile.phone = phone
            user.profile.save()

            
            messages.success(request, "Registration successful. Please login.")
            return redirect('accounts:login')
    else:
        form = RegisterForm()
        
    return render(request, 'accounts/register.html', {'form': form})



@login_required
def home_view(request):
    username = request.user.username
    api_url = "https://date.nager.at/api/v3/NextPublicHolidays/US"

    holidays = []
    try:
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            holidays = response.json()
        else:
            print(f"API returned status {response.status_code}")
    except requests.RequestException as e:
        print(f"Error fetching holidays: {e}")

    return render(request, 'accounts/home.html', {'username': username, 'holidays': holidays})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')
