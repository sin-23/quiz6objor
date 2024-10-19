from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib.auth import logout
from .models import Post, Report
from django.core.paginator import Paginator
from django.utils import timezone

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
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home if already logged in

    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')  # Get input

        # Attempt to find the user by email or username
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


@login_required

def create_post(request):

    if request.method == 'POST':

        content = request.POST.get('content')

        if content:

            post = Post.objects.create(user=request.user, content=content)

            messages.success(request, "Post created successfully.")

            return redirect('post_list')  # Redirect to the post list view

        else:

            messages.error(request, "Content cannot be empty.")

    return render(request, 'create_post.html')


@login_required

def post_list(request):

    posts = Post.objects.all().order_by('-created_at')  # Order by creation date

    paginator = Paginator(posts, 3)  # Show 3 posts per page

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)


    # Truncate content for display

    for post in page_obj:

        if len(post.content) > 100:

            post.truncated_content = post.content[:100] + '...'

        else:

            post.truncated_content = post.content


    return render(request, 'post_list.html', {'page_obj': page_obj})


@login_required

def report_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':

        message = request.POST.get('message')

        if message:

            Report.objects.create(post=post, user=request.user, message=message)

            messages.success(request, "Report submitted successfully.")

            return redirect('post_list')

        else:

            messages.error(request, "Please provide a message for the report.")

    return render(request, 'report_post.html', {'post': post})