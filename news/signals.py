import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import NewsUpdate

@receiver(post_save, sender=NewsUpdate)
def send_news_campaign(sender, instance, created, **kwargs):
    """ Trigger a news letter email to be send to all subscribers when a news update is uploaded. """
    if created:
        headers = {
            "Authorization": f"Bearer {settings.MAILERLITE_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }


        campaign_payload = {
            "name": f"News Update: {instance.title}",
            "subject": "New update from Maddocks Owlery",
            "type": "regular",
            "groups": [settings.MAILERLITE_GROUP_ID],
            "template": {
                "id": settings.MAILERLITE_TEMPLATE_ID
            }
        }

        create_response = requests.post(
            "https://connect.mailerlite.com/api/campaigns",
            json = campaign_payload,
            headers = headers
        )

        if create_response.status_code == 200:
            campaign_id = create_response.json().get('id')

            send_response = requests.post(
                f"https://connect.mailerlite.com/api/campaigns/{campaign_id}/actions/send",
                headers = headers
            )

            if send_response.status_code != 200:
                print("Failed to send campaign:", send_response.text)
        else:
            print("Failed to create campaign:", create_response.text)