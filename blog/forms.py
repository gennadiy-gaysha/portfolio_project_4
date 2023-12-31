from django import forms
from .models import Country, Post, Comment
from django_summernote.widgets import SummernoteWidget

# Creates a list of all countries form Country table
countries = Country.objects.all().values_list('country_name', 'country_name')
countries_list = []
for country in countries:
    countries_list.append(country)


class PostForm(forms.ModelForm):
    """
    A form used for creating and updating blog posts
    """

    def __init__(self, *args, **kwargs):
        """
        __init__: Initializes the form, setting up the queryset for the
        'country' field based on all the countries retrieved from the Country
        model, ordered by the 'country_name' attribute.
        Also, choices attribute of the 'status' field is set to a list of
        tuples, representing the restricted status choices for the post

        Inside the __init__ method, the super function is called, which calls
        the __init__ method of the parent class, in this case, forms.ModelForm
        """
        super(PostForm, self).__init__(*args, **kwargs)
        countries = Country.objects.all().order_by('country_name')
        self.fields['status'].choices = [(0, 'Save as draft'),
                                         (1, 'Send to moderation')]
        self.fields['country'].queryset = countries
        self.fields['featured_image']\
            .help_text = '<br><span style="color: green;">As the main post ' \
                         'image, *.png or *.jpg files with a size of up to ' \
                         '10MB are accepted. <br>All files should only be ' \
                         'in horizontal (landscape) orientation.</span>'

    class Meta:
        """
        The Meta class provides additional information about the form. It
        specifies the model to be used, along with the fields from the model
        that are to be included in the form.

        The widgets attribute of the Meta class is used to customize the
        appearance and behavior of the form fields. It defines the type of
        input for each field, along with the associated attributes to control
        their presentation in the form.

        """
        model = Post
        fields = (
        'country', 'title', 'featured_image', 'excerpt', 'content', 'status')

        widgets = {
            'country': forms.Select(choices=countries_list,
                                    attrs={'class': 'form-select',
                                           'style': 'width: 100%'}),
            'title': forms.TextInput(attrs={'class': 'form-control',
               'placeholder': 'Write your post title here'}),
            'featured_image': forms.FileInput(
                attrs={'class': 'form-control-file'}),
            'content': SummernoteWidget(attrs={'class': 'form-control'}),
            'excerpt': forms.Textarea(
                attrs={'class': 'form-control', 'style': 'height: 120px',
               'placeholder': 'Write your short summary or teaser here'}),
            'status': forms.Select(
                attrs={'class': 'form-select', 'style': 'width: 100%'})
        }




class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'style': 'height: 150px',
               'placeholder': 'Please leave your comment here'}))

    class Meta:
        model = Comment
        fields = ['body']
