from django import forms
from .models import User
from django.contrib.auth.hashers import make_password, check_password


class RegisterForm(forms.Form):

    username = forms.CharField(
        max_length=32,
        label='Username',
        error_messages={
            'required': 'Please type in your username.'
        }
    )

    email = forms.EmailField(
        max_length=64,
        label='Email address',
        error_messages={
            'required': 'Please type in your email address.'
        }
    )

    password = forms.CharField(
        max_length=64,
        label='Password',
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Please type in your password.'
        }
    )

    confirm_password = forms.CharField(
        max_length=64,
        label='Confirm password',
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Please confirm your password.'
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            # If passwords failed to match
            if password != confirm_password:
                self.add_error('confirm_password', 'Passwords do not match.')


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=32,
        label='Username',
        error_messages={
            'required': 'Please type in your username.'
        }
    )

    password = forms.CharField(
        max_length=64,
        label='Password',
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Please type in your password.'
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            # Check if username exists in DB
            try:
                user = User.objects.get(username=username)

                #  Check if password matches
                if not check_password(password, user.password):
                    self.add_error('password', 'Incorrect password')

            # if username does not exist in DB
            except User.DoesNotExist:
                self.add_error('username', 'Unregistered username.')
