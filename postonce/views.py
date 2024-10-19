from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib.auth import logout

def home(request):
    print("Home view accessed")
    return render(request, 'home.html')

def logout_view(request):
    logout(request)  # Log the user out
    messages.success(request, "You have been logged out successfully.")  # Success message
    return redirect('home')  # Redirect to home page after logout


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Hash the password before saving the user
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.is_active = False  # Set to inactive until admin approval
            user.save()

            messages.success(request, "Account created successfully! Please wait for admin approval.")
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home if already logged in

    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')  # Get input

        try:
            user = User.objects.get(email=username_or_email)  # Check if it's an email
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username_or_email)  # Check if it's a username
            except User.DoesNotExist:
                messages.error(request, "Invalid username or email.")  # Error message if not found
                return render(request, 'login.html')  # Re-render the login template

        # Log the user in without requiring a password
        login(request, user)
        messages.success(request, "Logged in successfully.")  # Success message
        return redirect('home')  # Redirect to home page after successful login

    return render(request, 'login.html')  # Render the login template


@login_required
def admin_dashboard(request):
    users = User.objects.all()  # Fetch all users
    return render(request, 'admin_dashboard.html', {'users': users})


@login_required
def approve_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True  # Approve the user account
    user.save()
    return redirect('admin_dashboard')  # Redirect back to the dashboard


@login_required
def reject_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()  # Remove the user account (or handle rejection differently)
    return redirect('admin_dashboard')  # Redirect back to the dashboard
