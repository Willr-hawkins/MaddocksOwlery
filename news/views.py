from django.shortcuts import render
from django.conf import settings

from .models import NewsUpdate

def news_updates_list(request):
    """ Display a list of all news updates uploaded to the site. """
    news_updates = NewsUpdate.objects.all().order_by('-date_created')

    context = {
        'news_updates': news_updates,
        'MEDIA_URL': settings.MEDIA_URL
    }

    return render(request, 'news/updates_list.html', context)