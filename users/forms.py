from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django import forms

from .models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите e-mail'
        })

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите username'
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите пароль повторно'
        })


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        exclude = []

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите e-mail'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите e-mail'
        })


class UserSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(UserSetPasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите новый пароль'
        })

        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите новый пароль повторно'
        })
