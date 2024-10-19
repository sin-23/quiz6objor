from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import User

@login_required  # Ensure that only logged-in users can access this view
def home(request):
    return render(request, 'home.html')  # Render the home template


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create the user but do not activate
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.is_active = False  # Set to inactive until admin approval
            user.save()

            messages.success(request, "Account created successfully! Please wait for admin approval.")
            return redirect('login')  # Redirect to login page or wherever you want
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']
        password = request.POST['password']

        # Authenticate user using username or email
        user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to a home page or dashboard after successful login
        else:
            messages.error(request, "Invalid username or password.")

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
