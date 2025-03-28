from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('authentication/', views.auth, name='Auth'),
    path('login/',views.user_login, name='User-Login'),
    path('register/',views.user_register, name='User-Register'),
    path('logout/',views.user_logout, name='User-Logout'),

    path('raise_complaint', views.raise_complaint, name='Raise-complaint'),

    path('submit_complaint', views.submit_complaint, name='Submit_complaint'),
    path('admin_dashboard/', views.admin_dashboard, name='Dashboard'),
    
]