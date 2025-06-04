from django.shortcuts import render
from django.conf import settings

from .models import GalleryImage

def gallery_view(request):
    images = list(GalleryImage.objects.all())
    
    # Split images into N roughly equal columns (e.g., 4)
    num_columns = 4
    columns = [[] for _ in range(num_columns)]
    for idx, image in enumerate(images):
        columns[idx % num_columns].append(image)

    context = {
        'images': images,
        'columns': columns,
        'MEDIA_URL': settings.MEDIA_URL
    }

    return render(request, 'gallery/gallery.html', context)
