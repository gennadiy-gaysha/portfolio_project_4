from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView

from .forms import PostForm
from .models import Post, Country


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
    form_class = PostForm

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
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePost(UpdateView):
    """
    A class-based view that allows the updating of an existing blog post.

    Attributes:
    model: The model used for updating the post, which is the Post model.
    form_class: The form class used for the update view, which is the PostForm.
    template_name: The template used for rendering the update post view,
    'blog/update_post'
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/update_post.html'

    def form_valid(self, form):
        """
        The method is executed when the submitted form data is valid. It saves the
        updated post and then redirects the user to the post-details page for the updated
        post.

        Args:
        form: The form that has valid data.

        Returns:
        A redirection to the post-details page for the updated post.
        """
        post = form.instance
        post.save()
        return redirect('post-details', slug=post.slug)


class DraftList(LoginRequiredMixin, generic.ListView):
    """
    View for displaying a list of drafts authored by the logged-in user.

    Attributes:
    model: The model to be used for retrieving draft posts, in this case, the Post model.
    template_name: The template used for rendering the draft list, 'blog/draft.html'.
    paginate_by: The number of items to include per page in the pagination.
    """
    model = Post
    template_name = 'blog/user_post_list.html'
    paginate_by = 3

    def get_queryset(self):
        """
        Method to retrieve the queryset of draft posts authored by the logged-in user.

        Returns:
        A queryset filtered by the current user and posts with status 0 (drafts), ordered
        by the creation date in descending order.
        """
        user = self.request.user
        return Post.objects.filter(author=user, status=0).order_by('-created_on')


class PublishedList(LoginRequiredMixin, generic.ListView):
    """
    Look at DraftList docstring
    """
    model = Post
    template_name = 'blog/user_post_list.html'
    paginate_by = 3

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user, status=2).order_by('-created_on')


class ModerationList(LoginRequiredMixin, generic.ListView):
    """
    Look at DraftList docstring
    """
    model = Post
    template_name = 'blog/user_post_list.html'
    paginate_by = 3

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user, status=1).order_by('-created_on')


class DeletePost(generic.DeleteView):
    """
    A generic view for deleting a blog post.

    Attributes:
    model: The model to be used for deleting the post, in this case, the Post model.
    template_name: The template used for rendering the confirmation page for deleting
    the post, 'blog/delete_post.html'.
    success_url: The URL to redirect to after the successful deletion of the post,
    using the reverse_lazy method.
    """
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('home')


def search_country(request):
    if request.method == 'POST':
        searched_country = request.POST.get('searched-country')
        countries = Country.objects.filter(country_name__icontains=searched_country)
        context = {'searched_country': searched_country, 'countries': countries}
        return render(request, 'blog/show_searched_results.html', context)
    else:
        return render(request, 'blog/show_searched_results.html')

class ShowCountry(generic.DetailView):
    model = Country
    template_name = 'blog/show_country.html'
