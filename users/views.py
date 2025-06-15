from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
import secrets
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from mailing_list_management_service.settings import EMAIL_HOST_USER
from users.forms import UserForm, UserRegisterForm, UserPasswordResetForm, UserSetPasswordForm
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, \
    PasswordResetConfirmView

from django.contrib.auth.models import Group


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('mail_management:main')


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('mail_management:main')


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()

        host = self.request.get_host()
        url = f'http://{host}/users/email_confirm/{token}'

        send_mail(
            subject='Подтверждение почты',
            message=f'Привет, спасибо за регистрацию! Перейди по ссылку для подтверждения почты: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        group = Group.objects.get(name='Пользователи')
        group.user_set.add(user)
        user.save()

        return super().form_valid(form)


def email_confirm(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm

    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy("users:password_reset_done")


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserSetPasswordForm

    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy("users:password_reset_complete")
