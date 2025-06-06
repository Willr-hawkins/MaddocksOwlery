from django.shortcuts import render, redirect, get_object_or_404
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
    """ Allow the logged in superuser to upload new images to the gallery page. """
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


@login_required
def delete_gallery_image(request, pk):
    """ Allow the logged in superuser to delete gallery images from the gallery page. """
    gallery_image = get_object_or_404(GalleryImage, pk=pk)

    if request.method == 'POST':
        gallery_image.delete()
        return redirect('gallery')
    
    context = {
        'gallery_image': gallery_image,
    }

    return render (request, 'gallery/delete_gallery_image.html', context)