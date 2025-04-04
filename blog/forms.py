from django import forms
from .models import Country, Post, Comment
from django_summernote.widgets import SummernoteWidget


class PostForm(forms.ModelForm):
    """
    A form used for creating and updating blog posts
    """

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        # Dynamically populate countries when the form is initialized
        countries = Country.objects.all().order_by('country_name')
        self.fields['country'].queryset = countries

        # Set status choices
        self.fields['status'].choices = [(0, 'Save as draft'),
                                         (1, 'Send to moderation')]

        # Add help text to image upload field
        self.fields['featured_image'].help_text = (
            '<br><span style="color: green;">As the main post '
            'image, *.png or *.jpg files with a size of up to '
            '10MB are accepted. <br>All files should only be '
            'in horizontal (landscape) orientation.</span>'
        )

        # Optional: Customize country select dropdown style
        self.fields['country'].widget.attrs.update({
            'class': 'form-select',
            'style': 'width: 100%'
        })

    class Meta:
        model = Post
        fields = ('country', 'title', 'featured_image', 'excerpt', 'content', 'status')

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post title here'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
            'content': SummernoteWidget(attrs={
                'class': 'form-control'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'height: 120px',
                'placeholder': 'Write your short summary or teaser here'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'style': 'width: 100%'
            })
        }


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'style': 'height: 150px',
               'placeholder': 'Please leave your comment here'}))

    class Meta:
        model = Comment
        fields = ['body']
