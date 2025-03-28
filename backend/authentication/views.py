from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
import base64
from .models import Complaint
from django.core.files.base import ContentFile
import base64
import uuid


# Create your views here.
os.environ["REPLICATE_API_TOKEN"] = "r8_3ppGXXZp8VSLLMgc37V1eLefKAPMVOr4GbCxO"

def home(request):
    return render(request, 'landing/base.html')

def auth(request):
    return render(request, 'landing/auth.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            messages.success(request, 'Login successful')
            return redirect('Home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect(f"{reverse('Auth')}?action=login")
    return render(request, 'landing/auth.html')

def user_register(request):
    special_characters = set("!@#$%^&*()_+-=[]{}|;:,.<>?~")
    if request.method == 'POST':
        username = request.POST.get('username','').strip()
        email = request.POST.get('email','').strip()
        password = request.POST.get('password','').strip()
        confirm_password = request.POST.get('confirm_password','').strip()

       
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, 'User already exists')
            return redirect(f"{reverse('Auth')}?action=signup")
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect(f"{reverse('Auth')}?action=signup")
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return redirect(f"{reverse('Auth')}?action=signup")
        elif not any (char.isdigit() for char in password):
            messages.error(request, 'Password must contain at least one digit')
            return redirect(f"{reverse('Auth')}?action=signup")
        elif not any (char.isupper() for char in password):
            messages.error(request, 'Password must contain at least one uppercase letter')
            return redirect(f"{reverse('Auth')}?action=signup")
        elif not any (char.islower() for char in password):
            messages.error(request, 'Password must contain at least one lowercase letter')
            return redirect(f"{reverse('Auth')}?action=signup")
        elif not any (char in special_characters for char in password):
            messages.error(request, 'Password must contain at least one special character')
            return redirect(f"{reverse('Auth')}?action=signup")
        
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request,user)
            messages.success(request, 'User created successfully')
            return redirect('Home')
    return render(request, 'landing/auth.html')


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logout successful')
        return redirect('Home')
    else:
        messages.error(request, 'You are not logged in')
        return redirect(f'{reverse("Auth")}?action=login')




def raise_complaint(request):

    return render(request, 'landing/raise_complaint.html')



@login_required
def submit_complaint(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        description = request.POST.get('description')
        image_data = None

        if 'cameraOutput' in request.POST and request.POST['cameraOutput']:
            image_base64 = request.POST['cameraOutput'].split(',')[1]
            image_data = base64.b64decode(image_base64)
            file_name = f"complaint_{uuid.uuid4().hex}.png"

        complaint = Complaint(
            location=location,
            description=description,
            user=request.user
        )

        if image_data:
            complaint.image.save(file_name, ContentFile(image_data), save=True)

        complaint.save()

        messages.success(request, 'Complaint submitted successfully!')
        return redirect('Home')

    return redirect('Home')


def admin_dashboard(request):
    complaint = Complaint.objects.all()

    context = {'complaints':complaint,

    }
    return render(request, 'landing/dashboard.html', context)