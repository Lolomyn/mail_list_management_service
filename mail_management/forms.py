from django import forms
from .models import MailRecipient, Message, Mailing


class MailRecipientsForm(forms.ModelForm):
    class Meta:
        model = MailRecipient
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(MailRecipientsForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите email'
        })

        self.fields['fullname'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите полное имя'
        })

        self.fields['commentary'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите комментарий'
        })


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields['email_subject'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите тему письма'
        })

        self.fields['email_body'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите текст письма'
        })


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)

        self.fields['first_submission_time'].widget = forms.DateInput(
            attrs={
                'class': 'form-control flatpickr-datetime',
                'placeholder': 'Выберите дату первой рассылки',
                'data-date-format': 'Y-m-d'
            }
        )

        self.fields['submission_time'].widget = forms.DateInput(
            attrs={
                'class': 'form-control flatpickr-datetime',
                'placeholder': 'Выберите дату окончания рассылки',
                'data-date-format': 'Y-m-d h-m-s'
            }
        )

        self.fields['status'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выберите статус рассылки'
        })

        self.fields['message'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выберите сообщение для рассылки'
        })

        self.fields['recipients'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выберите получателя рассылки'
        })
