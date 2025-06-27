from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.conf import settings
from .models import NewsUpdate
import unicodedata

@receiver(post_save, sender=NewsUpdate)
def notify_admin_on_create(sender, instance, created, **kwargs):
    if created:
        print(f"[DEBUG] Signal triggered: New NewsUpdate created with title: '{instance.title}'")

        subject = unicodedata.normalize("NFKD", f"News update for maddocksowlery.co.uk: {instance.title}").replace('\xa0', ' ')

        text_content = (
            f"Simon Maddocks has uploaded a News Update titled '{instance.title}' to the Maddocks Owlery website.\n\n"
            "Please review the content and change status to published.\n\n"
            "Along with sending out a newsletter."
        )

        # If you have a public URL for the news update or admin link, use it here
        # For example, if you have a named URL 'admin:news_newsupdate_change':
        try:
            admin_url = f"{settings.SITE_URL}" + reverse('admin:news_newsupdate_change', args=[instance.pk])
        except Exception:
            admin_url = "Admin URL not available"

        html_content = f"""
            <html>
                <body>
                    <h2>New News Update Created</h2>
                    <p><strong>Title:</strong> {instance.title}</p>
                    <p><strong>Created on:</strong> {instance.date_created.strftime('%Y-%m-%d %H:%M')}</p>
                    <p>{instance.content[:200]}{'...' if len(instance.content) > 200 else ''}</p>
                    <p>Please review and publish the update in the admin.</p>
                    <p><a href="https://www.maddocksowlery.co.uk/admin/news/newsupdate/">Go to News Update in Admin</a></p>
                    <hr>
                    <p>Remember to send out the newsletter when publishing!</p>
                </body>
            </html>
        """

        try:
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.EMAIL_HOST_USER,
                to=['hawkinswill02@gmail.com'],
            )
            email.attach_alternative(html_content, "text/html")
            email.encoding = 'utf-8'
            email.send(fail_silently=False)
            print("[DEBUG] Email sent successfully!")
        except Exception as e:
            print(f"[ERROR] Failed to send email: {e}")
