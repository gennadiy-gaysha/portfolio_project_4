from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic import CreateView

from .models import Post


class PostList(generic.ListView):
    """
    A view that displays a list of published blog posts on the home page.

    Attributes:
    model: The model used for retrieving data, in this case, the Post model.
    template_name: The template used for rendering the view, here, the
    'blog/home.html' template.
    queryset: The queryset used to retrieve all published posts, filtering the
    posts based on their status (status=2) and ordering them by their creation
    date in descending order.
    paginate_by: The number of posts displayed per page, set to 3 in this case.
    """
    model = Post
    template_name = 'blog/home.html'
    queryset = Post.objects.filter(status=2).order_by('-created_on')
    paginate_by = 3


class PostDetails(generic.DetailView):
    """
    A view that displays the detailed information of a specific blog post.

    Attributes:
    model: The model used for retrieving data, in this case, the Post model.
    template_name: The template used for rendering the view, here, the
    'blog/post_details.html' template.
    """
    model = Post
    template_name = 'blog/post_details.html'


class CreatePost(LoginRequiredMixin, CreateView):
    """
    A class-based view that enables the creation of a new blog post.

    Attributes:
    model: The model to be used for creating the post, in this case, the Post
    model.
    template_name: The template used for rendering the create post view,
    'blog/create_post.html'.
    fields: The fields from the model that are used for the form. These
    fields will be displayed in the template for the user to fill out.
    """
    model = Post
    template_name = 'blog/create_post.html'
    fields = ('title', 'featured_image', 'excerpt', 'content', 'status')

    def form_valid(self, form):
        """
        This method is being overriden in CreatePost view to provide custom
        logic that should be executed when the submitted form data is valid
        Automatically adds current logged-in user as the author of the post.

        Args:
        form: The form that is to be validated.

        Returns:
        super() is used to call the parent class's method. It calls the
        form_valid method of the parent class (CreateView) to ensure that
        the standard behavior of the CreateView is executed.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)

