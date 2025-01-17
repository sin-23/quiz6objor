# admin.py
from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'contact_number', 'is_active')
    list_filter = ('is_active',)

admin.site.register(User, UserAdmin)
