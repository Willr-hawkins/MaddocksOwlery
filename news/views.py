from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import NewsUpdate
from .forms import NewsUpdateForm

def news_updates_list(request):
    """ Display a list of all news updates uploaded to the site. """
    news_updates = NewsUpdate.objects.all().order_by('-date_created')

    context = {
        'news_updates': news_updates,
        'MEDIA_URL': settings.MEDIA_URL
    }

    return render(request, 'news/updates_list.html', context)

def news_update_details(request, pk):
    """ Displays the news updates content when the user clicks on the updates card, from the news updates list. """
    news_update = get_object_or_404(NewsUpdate, pk=pk)

    context = {
        'news_update': news_update,
    }

    return render(request, 'news/news_update_details.html', context)

@login_required
def create_news_update(request):
    """ Allow logged in superusers to upload new upadates directlty from the news page. """
    if request.method == 'POST':
        form = NewsUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news_updates_list')
    else:
        form = NewsUpdateForm()

    context = {
        'form': form,
    }

    return render(request, 'news/create_news_update.html', context)

@login_required
def edit_news_update(request, pk):
    """ allow logged in superuser to edit news updates from the news page. """
    
    news_update = get_object_or_404(NewsUpdate, pk=pk)

    if request.method == 'POST':
        form = NewsUpdateForm(request.POST, request.FILES, instance=news_update)
        if form.is_valid():
            form.save()
            return redirect('news_updates_list')
    else:
        form = NewsUpdateForm(instance=news_update)
        
    
    context = {
        'form': form,
    }

    return render (request, 'news/edit_news_update.html', context)