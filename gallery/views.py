from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import GalleryImage
from .forms import GalleryForm

def gallery_view(request):
    images = list(GalleryImage.objects.all())

    context = {
        'images': images,
        'MEDIA_URL': settings.MEDIA_URL
    }

    return render(request, 'gallery/gallery.html', context)

@login_required
def upload_gallery_image(request):
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery')
    else:
        form = GalleryForm()

    context = {
        'form': form,
    }
    return render(request, 'gallery/upload.html', context)
