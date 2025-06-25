import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import NewsUpdate

@receiver(post_save, sender=NewsUpdate)
def send_news_campaign(sender, instance, created, **kwargs):
    """ Create a MailerLite campaign and send it to newsletter subscribers when a news update is uploaded. """
    if not created:
        return

    headers = {
        "Authorization": f"Bearer {settings.MAILERLITE_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    #Payload to create campaign
    campaign_payload = {
        "name": f"News Update: {instance.title}",
        "type": "regular",
        "subject": f"New update from Maddocks Owlery: {instance.title}",
        "from": "news@maddocksowlery.com",
        "from_name": "Maddocks Owlery",
        "groups": [settings.MAILERLITE_GROUP_ID],
        "template_id": settings.MAILERLITE_TEMPLATE_ID,
    }

    #create campaign
    create_response = requests.post(
        "https://connect.mailerlite.com/api/campaigns",
        headers=headers,
        json=campaign_payload
    )

    if create_response.status_code not in [200, 201]:
        print("❌ Failed to create campaign:", create_response.text)
        return

    campaign_id = create_response.json().get("id")
    if not campaign_id:
        print("❌ No campaign ID returned")
        return

    #send the campaign
    send_response = requests.post(
        f"https://connect.mailerlite.com/api/campaigns/{campaign_id}/actions/send",
        headers=headers
    )

    if send_response.status_code in [200, 202]:
        print("✅ Campaign sent successfully.")
    else:
        print("❌ Failed to send campaign:", send_response.text)
    