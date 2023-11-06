from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth import authenticate

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError('Email field should not be empty')  
        try:
            validate_email(email)
        except forms.ValidationError:
            raise forms.ValidationError('Please enter a valid email')
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email already exists')
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username") 
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        password = self.cleaned_data.get("password")
        user.set_password(password) 
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not username or not password:
            raise forms.ValidationError('Username and password should not be empty')

        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('Invalid username or password')

        return cleaned_data