from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone

from users.models import User


class MailRecipient(models.Model):
    email = models.EmailField(
        max_length=150,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Email',
        help_text='Введите email получателя рассылки'
    )

    fullname = models.CharField(
        max_length=256,
        verbose_name='Фамилия Имя Отчество',
        help_text='Введите ФИО получателя рассылки'
    )

    commentary = models.TextField(
        blank=True,
        null=True,
        verbose_name='Комментарий',
        help_text='Введите комментарий'
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipients',
        verbose_name='Владелец записи'
    )

    def clean(self):
        try:
            validate_email(self.email)
        except ValidationError:
            raise ValidationError({'email': 'Введите корректный email адрес'})

    def __str__(self):
        return f'{self.fullname}:{self.email}'

    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылки'
        ordering = ['email', 'fullname']


class Message(models.Model):
    email_subject = models.CharField(
        max_length=256,
        help_text='Введите тему письма',
        verbose_name='Тема письма',
    )

    email_body = models.TextField(
        help_text='Введите текст письма',
        verbose_name='Тело письма'
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Создатель сообщения'
    )

    def __str__(self):
        return f'{self.email_subject}: {self.email_body}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['email_subject']


class Mailing(models.Model):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    ONCE = 'once'

    FREQUENCY_CHOICES = [
        (DAILY, 'Ежедневно'),
        (WEEKLY, 'Еженедельно'),
        (MONTHLY, 'Ежемесячно'),
        (ONCE, 'Один раз'),
    ]

    CREATE = 'Создана'
    START = 'Запущена'
    END = 'Завершена'

    MAILING_STATUS_CHOICES = [
        (CREATE, 'Создана'),
        (START, 'Запущена'),
        (END, 'Завершена')
    ]

    first_submission_time = models.DateTimeField(
        verbose_name='Дата и время первой отправки'
    )

    submission_time = models.DateTimeField(
        verbose_name='Дата и время окончания отправки'
    )

    last_sent = models.DateTimeField(
        verbose_name='Дата последней отправки',
        null=True,
        blank=True
    )

    frequency = models.CharField(
        max_length=7,
        choices=FREQUENCY_CHOICES,
        default=ONCE,
        verbose_name='Периодичность'
    )

    status = models.CharField(
        max_length=9,
        choices=MAILING_STATUS_CHOICES,
        default=CREATE,
        verbose_name='Статус рассылки'
    )

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='mailings'
    )

    recipients = models.ManyToManyField(
        MailRecipient,
        related_name='mailings'
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mailings',
        verbose_name='Создатель рассылки'
    )

    def get_recipients_count(self):
        return self.recipients.count()

    def update_status(self):
        now = timezone.now()

        if self.status != self.END and now > self.submission_time:
            self.status = self.END
            self.save()
        return self.status

    def can_be_sent(self):
        now = timezone.now()

        return (
                self.status != self.END and
                self.first_submission_time <= now <= self.submission_time
        )

    def save(self, *args, **kwargs):
        # При сохранении автоматически обновляем статус
        self.update_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Рассылка #{self.pk} - {self.message} ({self.get_status_display()})'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['message']


class MailingAttempt(models.Model):
    SUCCESS = 'success'
    FAILURE = 'failure'

    ATTEMPTS_CHOICES = [
        (SUCCESS, 'Успешно'),
        (FAILURE, 'Не успешно'),
    ]

    attempt_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время попытки'
    )

    status = models.CharField(
        max_length=7,
        choices=ATTEMPTS_CHOICES,
        verbose_name='Статус отправки рассылки'
    )

    mail_response = models.TextField(
        blank=True,
        null=True,
        verbose_name='Ответ почтового сервера'
    )
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name='Рассылка'
    )

    recipient = models.ForeignKey(
        MailRecipient,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Получатель'
    )

    def __str__(self):
        return (f"Попытка #{self.id} для рассылки #{self.mailing.id} - "
                f"{self.get_status_display()} ({self.attempt_datetime})")

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
        ordering = ['-attempt_datetime']
        indexes = [
            models.Index(fields=['mailing']),
            models.Index(fields=['status']),
            models.Index(fields=['attempt_datetime']),
        ]
