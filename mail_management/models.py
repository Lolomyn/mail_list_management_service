from django.db import models


class MailRecipient(models.Model):
    email = models.CharField(
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

    def __str__(self):
        return f'{self.email_subject}: {self.email_body}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['email_subject']


class Mailing(models.Model):
    first_submission_time = models.DateTimeField(
        verbose_name='Дата и время первой отправки'
    )

    submission_time = models.DateTimeField(
        verbose_name='Дата и время окончания отправки'
    )

    CREATE = 'Создана'
    START = 'Запущена'
    END = 'Завершена'

    MAILING_STATUS_CHOICES = [
        (CREATE, 'Создана'),
        (START, 'Запущена'),
        (END, 'Завершена')
    ]

    status = models.CharField(
        max_length=9,
        choices=MAILING_STATUS_CHOICES,
        default=CREATE,
        verbose_name='Статус рассылки'
    )

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='message'
    )

    recipients = models.ManyToManyField(
        MailRecipient,
        related_name='recipients'
    )

    def get_recipients_count(self):
        return self.recipients.count()

    def __str__(self):
        return f'{self.message}. Статус: {self.status}. Получатели: {self.recipients}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['message']
