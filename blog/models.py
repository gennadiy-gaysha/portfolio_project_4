from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.urls import reverse
from django.utils.text import slugify

STATUS = ((0, 'Draft'), (1, 'Moderation'), (2, 'Published'))


class Country(models.Model):
    iso = models.CharField(max_length=5, blank=True)
    iso3 = models.CharField(max_length=5, blank=True)
    iso_numeric = models.CharField(max_length=5, blank=True)
    fips = models.CharField(max_length=5, blank=True)
    country_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    capital = models.CharField(max_length=100, blank=True)
    area_sq_km = models.FloatField(default=0.0)
    population = models.IntegerField(default=0)
    continent = models.CharField(max_length=5, blank=True)
    tld = models.CharField(max_length=5, blank=True)
    currency_code = models.CharField(max_length=5, blank=True)
    currency_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    postal_code_format = models.CharField(max_length=100, blank=True)
    postal_code_regex = models.CharField(max_length=100, blank=True)
    languages = models.CharField(max_length=100, blank=True)
    geo_name_id = models.IntegerField(default=0)
    neighbours = models.CharField(max_length=100, blank=True)

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
        # explicitly calling the save method with super(Country, self).save(*args, **kwargs)
        # (instead of self.save() of the current instance) ensures avoiding recursion issue
        super().save(*args, **qwargs)


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    # Related_name='blog_posts' specifies the name to use for the reverse relation from
    # the User model back to the Post model.
    # user.blog_posts.all() - retrieves all the Post instances
    # that have that specific User instance as their author
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=False)

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
        super().save(*args, **qwargs)

    def get_absolute_url(self):
        """
        Calling the get_absolute_url method in Django templates or views
        generates the absolute URL for a specific model instance, e.g.
        <a href="{{ post.get_absolute_url }}"> generates
        http://127.0.0.1:8000/post/slug_name/

        get_absolute_url method provides the URL to which Django will redirect
        the user after the successful creation of a new post, allowing Django's
        built-in view handling to take care of the actual redirection to the
        post-details view and template. Slug here is from urls.py path:
        ('post/<slug:slug>/', views.PostDetails.as_view(), name='post-details')
        """
        return reverse('post-details', args=(str(self.slug),))


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
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
