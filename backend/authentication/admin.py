from django.contrib import admin

# Register your models here.
from .models import Complaint, Worker
admin.site.register(Complaint)
admin.site.register(Worker)
