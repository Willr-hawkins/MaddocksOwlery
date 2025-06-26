from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from .models import NewsUpdate
import unicodedata

@receiver(post_save, sender=NewsUpdate)
def notify_admin_on_create(sender, instance, created, **kwargs):
    """ Send an email to notify website creator of a news update being created. """

    if created:
        print(f"[DEBUG] Signal triggered: New NewsUpdate created with title: '{instance.title}'")

        raw_subject = f"News update for maddocksowlery.co.uk: {instance.title}"
        raw_message = (
            "Simon Maddocks has uploaded a News Update to the Maddocks Owlery website, "
            "please review the content and change status to published. "
            "Along with sending out a newsletter."
        )

        # Normalize unicode and strip problematic characters like non-breaking spaces.
        subject = unicodedata.normalize("NFKD", raw_subject).replace('\xa0', ' ')
        message = unicodedata.normalize("NFKD", raw_message).replace('\xa0', ' ')

        try:
            email = EmailMultiAlternatives(
                subject = subject_encoded,
                body = message,
                from_email = None,
                to = ['hawkinswill02@gmail.com'],
            )
            email.encoding = 'utf-8'
            email.send(fail_silently = False)
            print("[DEBUG] Email sent successfully!")
        except Exception as e:
            print(f"[ERROR] Failed to send email: {e}")
