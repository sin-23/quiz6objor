from django import forms
from .models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        min_length=8,  # Optional: Set minimum length for security
        help_text='Minimum 8 characters.'
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'contact_number']  # Remove password and confirm_password from here

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already in use.")
        return username

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if User.objects.filter(contact_number=contact_number).exists():
            raise forms.ValidationError("Contact number is already in use.")
        return contact_number

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
