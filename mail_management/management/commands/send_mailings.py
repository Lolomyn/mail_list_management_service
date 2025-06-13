from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from mail_management.models import Mailing, MailingAttempt
from datetime import timedelta


class Command(BaseCommand):
    help = 'Send scheduled mailings'

    def handle(self, *args, **options):
        now = timezone.now()
        mailings = Mailing.objects.filter(
            status=Mailing.START,
            first_submission_time__lte=now,
            submission_time__gte=now
        )

        for mailing in mailings:
            mailing.update_status()
            if not mailing.can_be_sent():
                continue

            recipients = mailing.recipients.all()
            success_count = 0

            for recipient in recipients:
                attempt = MailingAttempt(
                    mailing=mailing,
                    recipient=recipient,
                    attempt_datetime=now
                )

                try:
                    send_mail(
                        subject=mailing.message.email_subject,
                        message=mailing.message.email_body,
                        from_email=None,
                        recipient_list=[recipient.email],
                        fail_silently=False,
                    )
                    attempt.status = MailingAttempt.SUCCESS
                    attempt.mail_response = "Успешно отправлено"
                    success_count += 1
                except Exception as e:
                    attempt.status = MailingAttempt.FAILURE
                    attempt.mail_response = str(e)
                    self.stdout.write(self.style.ERROR(
                        f'Ошибка отправки для {recipient.email}: {str(e)}'
                    ))

                attempt.save()

            mailing.last_sent = now
            mailing.save()

            self.stdout.write(self.style.SUCCESS(
                f'Рассылка {mailing.pk} отправлена. Успешно: {success_count}/{recipients.count()}'
            ))
