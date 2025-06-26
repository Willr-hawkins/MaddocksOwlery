from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from storages.backends.s3boto3 import S3Boto3Storage
import unicodedata

class NewsUpdate(models.Model):
    """ Hold a database entry for a news updated on the owlery. """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', storage=S3Boto3Storage(), null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default= 'draft')

    def clean(self):
        # Normalize text fields to avoid non-breaking space errors, etc.
        self.title = unicodedata.normalize("NFKD", self.title).replace('\xa0', ' ').strip()
        self.content = unicodedata.normalize("NFKD", self.content).replace('\xa0', ' ').strip()

    def __str__(self):
        return self.title
