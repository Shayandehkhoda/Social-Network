from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError

class UserSignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise ValidationError('Email exists')
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        username_exists = User.objects.filter(username=username).exists()
        if username_exists:
            raise ValidationError('Username exists')
        return username

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=255, label='Username/Email')
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)


class UserInfoEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'bio', 'img', )