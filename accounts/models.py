from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from blog.models import Country


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = CloudinaryField ('image', default='placeholder')
    bio = models.TextField()
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'),
                                       ('Other', 'Other')])
    home_country = models.ForeignKey(Country, on_delete=models.CASCADE, null=False)
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


