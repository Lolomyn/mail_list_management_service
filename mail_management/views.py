import smtplib
from django.core.mail import EmailMessage

from django.shortcuts import render
from .models import MailRecipient, Message, Mailing, MailingAttempt
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import MailRecipientsForm, MessageForm, MailingForm
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone


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
    context_object_name = 'mailing'


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


class SendMailingView(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.update_status()

        if not mailing.can_be_sent():
            messages.error(request, 'Рассылка завершена или время отправки еще не наступило')
            return redirect('mail_management:mailing_detail', pk=pk)

        recipients = mailing.recipients.all()
        success_count = 0
        failure_count = 0

        for recipient in recipients:
            attempt = MailingAttempt(
                mailing=mailing,
                recipient=recipient,
                attempt_datetime=timezone.now()
            )

            try:
                email = EmailMessage(
                    subject=mailing.message.email_subject,
                    body=mailing.message.email_body,
                    to=[recipient.email],
                )
                email.send(fail_silently=False)

                attempt.status = MailingAttempt.SUCCESS
                attempt.mail_response = "Сообщение успешно отправлено"
                success_count += 1

            except smtplib.SMTPException as e:
                attempt.status = MailingAttempt.FAILURE
                attempt.mail_response = str(e)
                failure_count += 1
                messages.error(request, f'Ошибка отправки для {recipient.email}: {str(e)}')

            attempt.save()

        # Обновляем статус рассылки
        if mailing.status != Mailing.START:
            mailing.status = Mailing.START
            mailing.save()

        mailing.update_status()

        messages.success(
            request,
            f'Рассылка отправлена. Успешно: {success_count}, Неудачно: {failure_count}'
        )
        return redirect('mail_management:mailing_detail', pk=pk)


class MailingAttemptsView(ListView):
    model = MailingAttempt
    context_object_name = 'attempts'

    def get_queryset(self):
        mailing_id = self.kwargs['pk']
        return MailingAttempt.objects.filter(mailing_id=mailing_id).select_related('recipient')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing'] = get_object_or_404(Mailing, pk=self.kwargs['pk'])
        return context


def main(request):
    mailing_list = Mailing.objects.all()
    recipient_list = MailRecipient.objects.all()

    context = {
        'mailing_list': mailing_list,
        'recipient_list': recipient_list,
    }

    return render(request, 'mail_management/main.html', context=context)
