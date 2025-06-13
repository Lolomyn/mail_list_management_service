from django.urls import path
from . import views

app_name = 'mail_management'

urlpatterns = [
    path('', views.main, name='main'),

    path('recipient_list/', views.MailRecipientListView.as_view(), name='recipient_list'),
    path('recipients/<int:pk>/', views.MailRecipientDetailView.as_view(), name='recipient_detail'),
    path('recipients/<int:pk>/update/', views.MailRecipientUpdateView.as_view(), name='recipient_update'),
    path('create_recipient/', views.MailRecipientCreateView.as_view(), name='recipient_create'),
    path('recipients/<int:pk>/delete/', views.MailRecipientDeleteView.as_view(), name='recipient_delete'),

    path('message_list/', views.MessageListView.as_view(), name='message_list'),
    path('messages/<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('messages/<int:pk>/update/', views.MessageUpdateView.as_view(), name='message_update'),
    path('create_message/', views.MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/delete/', views.MessageDeleteView.as_view(), name='message_delete'),

    path('mailing_list/', views.MailingListView.as_view(), name='mailing_list'),
    path('mailings/<int:pk>/', views.MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/<int:pk>/update/', views.MailingUpdateView.as_view(), name='mailing_update'),
    path('create_mailing/', views.MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/delete/', views.MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailings/<int:pk>/send/', views.SendMailingView.as_view(), name='mailing_send'),

    path('mailings/<int:pk>/attempts/', views.MailingAttemptsView.as_view(), name='mailing_attempts_list'),
]
