from django.contrib import admin
from .models import MailRecipient, Message, Mailing


@admin.register(MailRecipient)
class MailRecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'fullname', 'commentary',)
    list_filter = ('email', 'fullname',)
    search_fields = ('email', 'fullname',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('email_subject', 'email_body',)
    list_filter = ('email_subject',)
    search_fields = ('email_subject', 'email_body',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('first_submission_time', 'submission_time', 'status', 'message', 'get_recipients_count')
    list_filter = ('status', 'message',)
    search_fields = ('message',)
