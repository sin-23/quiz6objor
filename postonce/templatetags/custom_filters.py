# quiz6sana/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def obfuscate_username(username):
    if not username:
        return ""
    # Example logic to obfuscate username
    return username[:3] + '***' + username[-3:]  # e.g., "admin123" -> "adm***123"
