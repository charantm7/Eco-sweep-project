from django.contrib import admin

# Register your models here.
from .models import Complaint, Worker, CleanedPhoto
admin.site.register(Complaint)
admin.site.register(Worker)
admin.site.register(CleanedPhoto)
