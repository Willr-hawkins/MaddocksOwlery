from django import forms
from .models import NewsUpdate

class NewsUpdateForm(forms.ModelForm):
    """ Form to upload a news upadate to the news page. """
    class Meta:
        model = NewsUpdate
        fields = [
            'title',
            'content',
            'image',
        ]