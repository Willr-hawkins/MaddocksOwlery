import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import NewsUpdate

@receiver(post_save, sender=NewsUpdate)
def send_news_campaign(sender, instance, created, **kwargs):
    """ Trigger a news letter email to be send to all subscribers when a news update is uploaded. """
    if not created:
        return

    headers = {
        "Authorization": f"Bearer {settings.MAILERLITE_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Fetch all subscribers from the MailerLite group, handling pagination
    group_id = settings.MAILERLITE_GROUP_ID
    page = 1
    emails = []

    while True:
        response = requests.get(
            f"https://connect.mailerlite.com/api/groups/{group_id}/subscribers?page={page}",
            headers=headers
        )

        if response.status_code != 200:
            print(f"❌ Failed to fetch subscribers (page {page}):", response.text)
            return

        data = response.json()
        subscribers = data.get("data", [])
        if not subscribers:
            break  # No more subscribers to fetch

        emails.extend([sub["email"] for sub in subscribers])

        meta = data.get("meta", {})
        total_pages = meta.get("pagination", {}).get("total_pages", 1)
        if page >= total_pages:
            break
        page += 1

    if not emails:
        print("❌ No subscribers found in the group.")
        return

    # Create the campaign
    campaign_payload = {
        "name": f"News Update: {instance.title}",
        "type": "regular",
        "subject": "New update from Maddocks Owlery",
        "from": "news@maddocksowlery.com",
        "from_name": "Maddocks Owlery",
        "emails": emails,
        "template_id": settings.MAILERLITE_TEMPLATE_ID
    }

    response = requests.post(
        "https://connect.mailerlite.com/api/campaigns",
        json=campaign_payload,
        headers=headers
    )

    if response.status_code in [200, 201]:
        campaign_id = response.json().get("id")
        send_response = requests.post(
            f"https://connect.mailerlite.com/api/campaigns/{campaign_id}/actions/send",
            headers=headers
        )
        if send_response.status_code not in [200, 202]:
            print("❌ Failed to send campaign:", send_response.text)
    else:
        print("❌ Failed to create campaign:", response.text)