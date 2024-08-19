from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Profile


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email')
        labels = {
            'username': 'Username* ',
            'email': 'Email@ ',
        }
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'elon@musk.com...', 'class': 'font2  '}),
            'password': forms.PasswordInput(attrs={'class': 'font2 ', 'autocomplete': 'password'}),
            'password2': forms.PasswordInput(attrs={'class': 'font2  m-0', 'autocomplete': 'password'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', ]
        labels = {
            'realname': 'Name'
        }
        widgets = {
            'image': forms.FileInput(),
            'bio': forms.Textarea(attrs={'rows': 2}),
        }
