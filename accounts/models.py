from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = CloudinaryField ('image', default='placeholder')
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'),
                                       ('Other', 'Other')], blank=True)
    home_country = models.CharField(max_length=100, blank=True)
    instagram_profile = models.URLField(blank=True)
    twitter_profile = models.URLField(blank=True)
    facebook_profile = models.URLField(blank=True)
    linkedin_profile = models.URLField(blank=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        """
        Utilizes the `reverse` function to generate the URL using the 'author-bio'
        view along with the corresponding user's identifier as an argument.
        """
        return reverse('author-bio', args=(str(self.user),))


