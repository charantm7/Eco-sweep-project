from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
import base64
from .models import Complaint, Worker
from django.core.files.base import ContentFile
import base64
import uuid
from geopy.geocoders import Nominatim
from django.http import JsonResponse
from geopy.exc import GeocoderTimedOut
from django.contrib import messages
from .forms import WorkerForm


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
        name = request.POST.get('name')
        location = request.POST.get('location')
        description = request.POST.get('description')
        image_data = None

        if 'cameraOutput' in request.POST and request.POST['cameraOutput']:
            image_base64 = request.POST['cameraOutput'].split(',')[1]
            image_data = base64.b64decode(image_base64)
            file_name = f"complaint_{uuid.uuid4().hex}.png"

        complaint = Complaint(
            name=name,
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

def get_location_name(request):
    latitude = request.GET.get('lat')
    longitude = request.GET.get('lon')

    if not latitude or not longitude:
        return JsonResponse({"error": "Invalid coordinates"}, status=400)

    try:
        # Use a unique user_agent to avoid being blocked
        geolocator = Nominatim(user_agent="your_app_name", timeout=10)  
        location = geolocator.reverse((latitude, longitude), exactly_one=True)

        if location and location.address:
            return JsonResponse({"address": location.address})
        else:
            return JsonResponse({"error": "Location not found"}, status=404)

    except GeocoderTimedOut:
        return JsonResponse({"error": "Geocoding service timed out"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def profile(request, u_name):
    user = User.objects.get(username=request.user.username)
    complaint = Complaint.objects.filter(user=user)
    u_name = user
    return render(request, 'landing/profile.html', {'user':user, 'complaints':complaint})


@login_required
def add_worker(request):
    if request.method == "POST":
        form = WorkerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Worker added successfully!")
            return redirect("Home")  # Change this to your admin panel URL
    else:
        form = WorkerForm()
    
    return render(request, "landing/add_worker.html", {"form": form})

@login_required
def worker_dashboard(request):
    # Fetch complaints assigned to the logged-in worker
    assigned_complaints = Complaint.objects.filter(worker=request.user.worker_profile)
    return render(request, 'landing/worker_dashboard.html', {'assigned_complaints': assigned_complaints})


@login_required
def update_complaint_status(request, complaint_id):
    if request.method == "POST":
        complaint = Complaint.objects.get(id=complaint_id)

        if complaint.worker == request.user.worker_profile:
            new_status = request.POST.get('status')
            complaint.status = new_status
            complaint.save()
            messages.success(request, "Complaint status updated successfully!")
        else:
            messages.error(request, "You are not authorized to update this complaint.")

    return redirect('worker_dashboard')

def delete_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if request.method == 'POST':
        complaint.delete()
        messages.success(request, 'Complaint deleted successfully!')
    return redirect('Dashboard') 

def assign_worker(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    workers = Worker.objects.all()

    if request.method == 'POST':
        worker_id = request.POST.get('worker')
        if worker_id:
            complaint.worker = get_object_or_404(Worker, id=worker_id)
            complaint.status = "In Progress"  # Auto-update status
            complaint.save()
            messages.success(request, f'Complaint assigned to {complaint.worker.user.username}!')
        else:
            messages.error(request, "Please select a worker.")

        return redirect('Dashboard')  # Redirect to the complaint list page

    return render(request, 'landing/assign.html', {'complaint': complaint, 'workers': workers}) 