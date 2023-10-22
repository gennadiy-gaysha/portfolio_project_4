from django.views import generic
from .models import Post


class PostList(generic.ListView):
    """
    A view that displays a list of published blog posts on the home page.

    Attributes:
    model: The model used for retrieving data, in this case, the Post model.
    template_name: The template used for rendering the view, here, the 'blog/home.html' template.
    queryset: The queryset used to retrieve all published posts, filtering the posts based
    on their status (status=2) and ordering them by their creation date in descending order.
    paginate_by: The number of posts displayed per page, set to 3 in this case.
    """
    model = Post
    template_name = 'blog/home.html'
    queryset = Post.objects.filter(status=2).order_by('-created_on')
    paginate_by = 3
