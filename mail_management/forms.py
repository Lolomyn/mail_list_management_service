from django import forms
from .models import MailRecipient, Message, Mailing
from django.utils import timezone


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
        widgets = {
            'first_submission_time': forms.DateTimeInput(
                format='%Y-%m-%d %H:%M',
                attrs={
                    'class': 'form-control flatpickr-datetime',
                    'placeholder': 'Выберите дату и время первой рассылки',
                }
            ),
            'submission_time': forms.DateTimeInput(
                format='%Y-%m-%d %H:%M',
                attrs={
                    'class': 'form-control flatpickr-datetime',
                    'placeholder': 'Выберите дату и время окончания рассылки',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)

        self.fields['first_submission_time'].input_formats = ['%Y-%m-%d %H:%M']
        self.fields['submission_time'].input_formats = ['%Y-%m-%d %H:%M']

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

    def clean(self):
        cleaned_data = super().clean()
        first_submission_time = cleaned_data.get('first_submission_time')
        submission_time = cleaned_data.get('submission_time')

        if first_submission_time and submission_time:
            if first_submission_time > submission_time:
                raise forms.ValidationError(
                    "Время окончания отправки не может быть раньше времени начала"
                )

            if submission_time < timezone.now():
                raise forms.ValidationError(
                    "Время окончания отправки не может быть в прошлом"
                )

        return cleaned_data
