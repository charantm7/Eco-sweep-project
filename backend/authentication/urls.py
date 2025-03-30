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
    path('get-location/', views.get_location_name, name='get_location_name'),

    path('profile/<str:u_name>/', views.profile, name='Profile'),

    path('add-worker/', views.add_worker, name='add_worker'),
    path('assign-worker/<int:complaint_id>/', views.assign_worker, name='assign_worker'),


    path('worker/dashboard/', views.worker_dashboard, name="worker_dashboard"),
    path('worker/update-complaint/<int:complaint_id>/', views.update_complaint_status, name="update_complaint_status"),

     path('complaint/delete/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
     

     path('cleaned/',views.cleaned, name='Cleaned'),

      path('review_cleaned_photo/<int:photo_id>/', views.review_cleaned_photo, name='review_cleaned_photo'),
     
]

      

    
