from django.shortcuts import render
from .models import MailRecipient, Message, Mailing
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import MailRecipientsForm, MessageForm, MailingForm


class MailRecipientListView(ListView):
    model = MailRecipient


class MailRecipientCreateView(CreateView):
    model = MailRecipient
    form_class = MailRecipientsForm
    success_url = reverse_lazy('mail_management:recipient_list')


class MailRecipientUpdateView(UpdateView):
    model = MailRecipient
    form_class = MailRecipientsForm
    success_url = reverse_lazy('mail_management:recipient_detail')

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('mail_management:recipient_detail', kwargs={'pk': pk})


class MailRecipientDeleteView(DeleteView):
    model = MailRecipient
    success_url = reverse_lazy('mail_management:recipient_list')


class MailRecipientDetailView(DetailView):
    model = MailRecipient


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mail_management:message_detail')

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('mail_management:message_detail', kwargs={'pk': pk})


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mail_management:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mail_management:message_list')


class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mail_management:mailing_detail')

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('mail_management:mailing_detail', kwargs={'pk': pk})


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mail_management:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mail_management:mailing_list')
