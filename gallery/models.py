from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

class GalleryImage(models.Model):
    """ Hold a database entry for a gallery image with the description. """
    image = models.ImageField(upload_to='gallery/', storage=S3Boto3Storage(), null=False, blank=False)
    description = models.TextField()

