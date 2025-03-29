from django.db import models
from django.contrib.auth.models import User

# Create your models here.





class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="worker_profile")
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    skills = models.TextField(null=True, blank=True)  # Optional: Worker skills
    availability = models.BooleanField(default=True)  # Available for new assignments
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    



class Complaint(models.Model):
    name = models.CharField(null=True,blank=True,max_length=20 )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_complaints", null=True)
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, related_name="assigned_complaints", null=True, blank=True)
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    image = models.ImageField(upload_to="complaint_images/", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')],
        default='Pending'
    )

    def __str__(self):
        return f"Complaint {self.id} - {self.status}"
    
class CleanedPhoto(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='cleaned_photos')
    image = models.ImageField(upload_to='cleaned_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    admin_comment = models.TextField(blank=True, null=True)