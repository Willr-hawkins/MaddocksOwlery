from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import NewsUpdate
import unicodedata

@receiver(post_save, sender=NewsUpdate)
def notify_admin_on_create(sender, instance, created, **kwargs):
    if created:
        print(f"[DEBUG] Signal triggered: New NewsUpdate created with title: '{instance.title}'")

        raw_subject = f"News update for maddocksowlery.co.uk: {instance.title}"
        raw_message = (
            "Simon Maddocks has uploaded a News Update to the Maddocks Owlery website, "
            "please review the content and change status to published. "
            "Along with sending out a newsletter."
        )

        subject = unicodedata.normalize("NFKD", raw_subject).replace('\xa0', ' ')
        subject = subject.encode('utf-8', 'ignore').decode('utf-8')

        message = unicodedata.normalize("NFKD", raw_message).replace('\xa0', ' ')
        message = message.encode('utf-8', 'ignore').decode('utf-8')

        from_email = unicodedata.normalize("NFKD", settings.EMAIL_HOST_USER).replace('\xa0', ' ')
        from_email = from_email.encode('utf-8', 'ignore').decode('utf-8')

        print("[DEBUG] subject repr:", repr(subject))
        print("[DEBUG] message repr:", repr(message))
        print("[DEBUG] from_email repr:", repr(from_email))

        try:
            email = EmailMultiAlternatives(
                subject=subject,
                body=message,
                from_email=from_email,
                to=['hawkinswill02@gmail.com'],
            )
            email.encoding = 'utf-8'
            email.content_subtype = "plain"  # explicitly plain text
            email.send(fail_silently=False)
            print("[DEBUG] Email sent successfully!")
        except Exception as e:
            print(f"[ERROR] Failed to send email: {e}")