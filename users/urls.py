from django.urls import path
from users.apps import UsersConfig
from django.contrib.auth.views import LogoutView, LoginView
from . import views

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('email_confirm/<str:token>/', views.email_confirm, name='email_confirm')
]
