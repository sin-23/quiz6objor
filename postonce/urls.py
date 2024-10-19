from django.urls import path
from . import views  # Correctly import all views from the current directory


urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login_view, name='login'),  # Login view
    path('home/', views.home, name='home'),  # Home view after login
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard URL
    path('admin_dashboard/approve/<int:user_id>/', views.approve_user, name='approve_user'),  # Approve URL
    path('admin_dashboard/reject/<int:user_id>/', views.reject_user, name='reject_user'),  # Reject URL
]

