from django.db import models
from django.utils import timezone
from storages.backends.s3boto3 import S3Boto3Storage

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

    def __str__(self):
        return self.title
