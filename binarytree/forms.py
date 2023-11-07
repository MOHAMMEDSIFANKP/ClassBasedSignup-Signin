from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError('Email field should not be empty')  
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('Please enter a valid email')
        
        if User.objects.filter(email=email).exists():
            raise ValidationError('email already exists')
        return email

    
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not username or not password:
            raise forms.ValidationError('Username and password should not be empty')
        return cleaned_data