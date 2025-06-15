from django.contrib import admin
from .models import MailRecipient, Message, Mailing, MailingAttempt


@admin.register(MailRecipient)
class MailRecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'fullname', 'commentary', 'created_by')
    list_filter = ('email', 'fullname',)
    search_fields = ('email', 'fullname',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('email_subject', 'email_body', 'created_by')
    list_filter = ('email_subject',)
    search_fields = ('email_subject', 'email_body',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        'first_submission_time', 'submission_time', 'status', 'message', 'get_recipients_count', 'created_by')
    list_filter = ('status', 'message',)
    search_fields = ('message',)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = (
        'attempt_datetime', 'status', 'mail_response', 'mailing', 'recipient')
    list_filter = ('status',)
    search_fields = ()
