from django.urls import path
from . import views  # Correctly import all views from the current directory


urlpatterns = [
    path('register/', views.register, name='register'),  # Registration view
    path('login/', views.login_view, name='login'),  # Login view
    path('', views.home, name='home'),  # Home view after login
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard URL
    path('admin_dashboard/approve/<int:user_id>/', views.approve_user, name='approve_user'),  # Approve URL
    path('admin_dashboard/reject/<int:user_id>/', views.reject_user, name='reject_user'),  # Reject URL
    path('logout/', views.logout_view, name='logout'),  # Logout view
    path('create/', views.create_post, name='create_post'),
    path('', views.post_list, name='post_list'),  # Assuming this is the home page
    path('report/<int:post_id>/', views.report_post, name='report_post')
]

