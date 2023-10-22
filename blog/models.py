from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.text import slugify

STATUS = ((0, 'Draft'), (1, 'Moderation'), (2, 'Published'))


class Country(models.Model):
    iso = models.CharField(max_length=5, default='')
    iso3 = models.CharField(max_length=5, default='')
    iso_numeric = models.CharField(max_length=5, default='')
    fips = models.CharField(max_length=5, default='')
    country_name = models.CharField(max_length=100, unique=True, default='')
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    capital = models.CharField(max_length=100, default='')
    area_sq_km = models.FloatField(default=0.0)
    population = models.IntegerField(default=0)
    continent = models.CharField(max_length=5, default='')
    tld = models.CharField(max_length=5, blank=True, default='')
    currency_code = models.CharField(max_length=5, default='')
    currency_name = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=100, default='')
    postal_code_format = models.CharField(max_length=100, default='')
    postal_code_regex = models.CharField(max_length=100, default='')
    languages = models.CharField(max_length=100, default='')
    geo_name_id = models.IntegerField(default=0)
    neighbours = models.CharField(max_length=100, default='')

    def __str__(self):
        """
        Method represents a class's objects as a string. Defines how
        an instance of a class should be printed as a string.
        """
        return self.country_name

    def save(self, *args, **qwargs):
        """
        Save method of the model is being overriden. Inside the save method,
        the condition if the slug is not already set is checked.
        If it's blank, a slug from the title is generated using slugify and then
        saved in the model. This ensures that the slug is automatically created
        from the title when a new Country instance is created.
        """
        if not self.slug:
            self.slug = slugify(self.country_name)
        self.save(*args, **qwargs)


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    # Related_name='blog_posts' specifies the name to use for the reverse relation from
    # the User model back to the Post model.
    # user.blog_posts.all() - retrieves all the Post instances
    # that have that specific User instance as their author
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        """
        Method represents a class's objects as a string. Defines how
        an instance of a class should be printed as a string.
        """
        return self.title

    def number_of_likes(self):
        """
        Helper method that returns total number of likes on a Post
        """
        return self.likes.count()

    def save(self, *args, **qwargs):
        """
        Save method of the model is being overriden. Inside the save method,
        the condition if the slug is not already set is checked.
        If it's blank, a slug from the title is generated using slugify and then
        saved in the model. This ensures that the slug is automatically created
        from the title when a new Post instance is created.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        self.save(*args, **qwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        """
        Method represents a class's objects as a string. Defines how
        an instance of a class should be printed as a string.
        """
        return f'Comment {self.body} by {self.name}'
