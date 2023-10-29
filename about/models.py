from django.db import models
from cloudinary.models import CloudinaryField


class About(models.Model):
    title    = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')

    def __str__(self):
        return self.title
