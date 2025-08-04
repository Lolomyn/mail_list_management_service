from django.urls import path
from users.apps import UsersConfig
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetDoneView, PasswordResetCompleteView
from . import views

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('email_confirm/<str:token>/', views.email_confirm, name='email_confirm'),

    path('password_reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    path('user_detail/', views.UserListView.as_view(), name='user_detail'),
    path('user_update/', views.CurrentUserUpdateView.as_view(), name='user_update')
]
