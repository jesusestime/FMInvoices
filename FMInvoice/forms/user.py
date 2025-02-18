from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    """Form for user registration"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomUserChangeForm(UserChangeForm):
    """Form for updating user information"""
    password = None  # Hide password field

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UserActivationForm(UserChangeForm):
    """Form for activating or managing user permissions"""
    class Meta:
        model = User
        fields = ['is_active', 'is_staff', 'is_superuser']


class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form"""
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput())


class CustomPasswordChangeForm(PasswordChangeForm):
    """Form for changing password"""
    pass


class CustomPasswordResetForm(PasswordResetForm):
    """Form for resetting password"""
    pass


class CustomSetPasswordForm(SetPasswordForm):
    """Form for setting a new password"""
    pass
