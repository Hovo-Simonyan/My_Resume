from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from ckeditor.fields import RichTextFormField
from .models import *


class AddResumeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['language'].empty_label = 'Язык не выбран'

    class Meta:
        model = Resume
        fields = ['name', 'surname', 'age', 'city', 'position', 'email', 'facebook', 'telegram', 'phone_number',
                  'content', 'photo', 'is_published', 'language']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-only-name'}),
            'position': forms.TextInput(attrs={'class': 'form-only-name', 'placeholder': 'Должность (например Django Python Developer)'}),
            'facebook': forms.URLInput(attrs={'class': 'form-only-name'}),
            'telegram': forms.TextInput(attrs={'class': 'form-only-name'}),
            'surname': forms.TextInput(attrs={'class': 'form-only-name'}),
            'age': forms.NumberInput(attrs={'class': 'form-only-name'}),

            'email': forms.EmailInput(attrs={'class': 'form-only-name'}),
            'city': forms.TextInput(attrs={'class': 'form-only-name'}),
            'content': RichTextFormField(),
            'phone_number': forms.TextInput(attrs={'class': 'form-only-name'}),
            'photo': forms.FileInput(attrs={'class': 'mb-3 form-label form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check form-check-input form-check-label'}),
            'language': forms.Select(attrs={'class': 'btn btn-outline-success'}),
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'mb-3 form-label form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'mb-3 form-label form-control'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'mb-3 form-label form-control'}))
    password2 = forms.CharField(label='Повтор пароля',
                                widget=forms.PasswordInput(attrs={'class': 'mb-3 form-label form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'mb-3 form-label form-control'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'mb-3 form-label form-control'}))
