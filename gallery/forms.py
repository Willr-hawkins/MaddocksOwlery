from django import forms
from .models import GalleryImage

class GalleryForm(forms.ModelForm):
    """ Form to upload images to the gallery. """
    class Meta:
        model = GalleryImage
        fields = [
            'image',
            'description'
        ]