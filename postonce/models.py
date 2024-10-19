from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username, contact_number, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        if not contact_number:
            raise ValueError("Users must have a contact number")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            contact_number=contact_number,
        )
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, contact_number, password):
        user = self.create_user(
            email,
            username=username,
            contact_number=contact_number,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    contact_number = models.CharField(max_length=15, unique=True)

    # Additional fields for account activation
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'contact_number']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set field to now when created

    def __str__(self):
        return f"Post by {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"



class Report(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.user.username} on {self.created_at}"
