from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.views.generic import CreateView, UpdateView
from .forms import CommentForm

from .filters import PostFilter
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

    def get_queryset(self):
        """
        Get the filtered queryset of Post objects based on the request parameters.

        Filters the queryset of Post objects by the 'status' field with a value of 2.
        Orders the queryset by the 'created_on' field in descending order.
        Applies the filters specified in the PostFilter class based on the request parameters.

        Returns:
            queryset:
                The filtered queryset of Post objects based on the applied filters.
        """
        queryset = Post.objects.filter(status=2).order_by('-created_on')
        filter_data = PostFilter(self.request.GET, queryset=queryset)
        return filter_data.qs

    def get_context_data(self, **kwargs):
        """
        Get the context data for rendering the template.

        Retrieves the context data using the superclass get_context_data method.
        Adds the 'filter' key to the context with the PostFilter object, allowing
        the filter form to be accessible in the template.

        Args:
            **kwargs: dict
                Arbitrary keyword arguments.

        Returns:
            dict:
                The context data for rendering the template, including the 'filter'
                key for the PostFilter object.
        """
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())
        return context


class PostDetails(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(request, 'blog/post_details.html',
                      {'post': post, 'comments': comments,
                       'liked': liked, 'comment_form': CommentForm(),
                       'commented': False}, )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=2)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(request, 'blog/post_details.html',
                      {'post': post, 'comments': comments,
                       'liked': liked, 'comment_form': CommentForm(),
                       'commented': True}, )


class PostLike(View):
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post-details', args=[slug]))


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
        messages.success(self.request, 'Post created successfully. Please '
                                       'await approval if you sent it to '
                                       'moderation.')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Error in {field}: {error}')
                return super().form_invalid(form)


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

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        # Checks if the user is authenticated and has the permission to
        # change the post
        if not request.user.is_authenticated \
                or not request.user == post.author:
            raise PermissionDenied  # Triggers permission_denied view
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """
        The method is executed when the submitted form data is valid. It saves
        the updated post and then redirects the user to the post-details page
        for the updated post.

        Args:
        form: The form that has valid data.

        Returns:
        A redirection to the post-details page for the updated post.
        """
        post = form.instance
        post.save()
        messages.success(self.request, 'Post updated successfully. Please, '
                                       'await approval if you sent it to '
                                       'moderation')
        return redirect('post-details', slug=post.slug)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Error in {field}: {error}')
                return super().form_invalid(form)


class DraftList(LoginRequiredMixin, generic.ListView):
    """
    View for displaying a list of drafts authored by the logged-in user.

    Attributes:
    model: The model to be used for retrieving draft posts, in this case, the
    Post model.
    template_name: The template used for rendering the draft list,
    'blog/draft.html'.
    paginate_by: The number of items to include per page in the pagination.
    """
    model = Post
    template_name = 'blog/user_post_list.html'
    paginate_by = 3

    def get_queryset(self):
        """
        Method to retrieve the queryset of draft posts authored by the
        logged-in user.

        Returns:
        A queryset filtered by the current user and posts with status 0
        (drafts), ordered by the creation date in descending order.
        """
        user = self.request.user
        return Post.objects.filter(author=user, status=0).order_by(
            '-created_on')

    def dispatch(self, request, *args, **kwargs):
        username = kwargs.get('username', None)
        if request.user.username != username or \
                not request.user.is_authenticated:
            raise PermissionDenied  # Triggers permission_denied view
        return super().dispatch(request, *args, **kwargs)


class PublishedList(LoginRequiredMixin, generic.ListView):
    """
    Look at DraftList docstring
    """
    model = Post
    template_name = 'blog/user_post_list.html'
    paginate_by = 3

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user, status=2).order_by(
            '-created_on')

    def dispatch(self, request, *args, **kwargs):
        username = kwargs.get('username', None)
        if request.user.username != username or \
                not request.user.is_authenticated:
            raise PermissionDenied  # Triggers permission_denied view
        return super().dispatch(request, *args, **kwargs)


class ModerationList(LoginRequiredMixin, generic.ListView):
    """
    Look at DraftList docstring
    """
    model = Post
    template_name = 'blog/user_post_list.html'
    paginate_by = 3

    def dispatch(self, request, *args, **kwargs):
        username = kwargs.get('username', None)
        if request.user.username != username or \
                not request.user.is_authenticated:
            raise PermissionDenied  # Triggers permission_denied view
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user, status=1).order_by(
            '-created_on')


class DeletePost(generic.DeleteView):
    """
    A generic view for deleting a blog post.

    Attributes:
    model: The model to be used for deleting the post, in this case, the Post
    model.
    template_name: The template used for rendering the confirmation page for
    deleting the post, 'blog/delete_post.html'.
    success_url: The URL to redirect to after the successful deletion of the
    post, using the reverse_lazy method.
    """
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        # Checks if the user is authenticated and has the permission to
        # change the post
        if not request.user.is_authenticated \
                or not request.user == post.author:
            raise PermissionDenied  # Triggers permission_denied view
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Post deleted successfully.')
        return super().delete(request, *args, **kwargs)


def search_country(request):
    if request.method == 'POST':
        searched_country = request.POST.get('searched-country')
        countries = Country.objects.filter(
            country_name__icontains=searched_country).order_by('country_name')
        context = {'searched_country': searched_country,
                   'countries': countries}
        return render(request, 'blog/show_searched_results.html', context)
    else:
        return render(request, 'blog/show_searched_results.html')


class ShowCountry(generic.DetailView):
    model = Country
    template_name = 'blog/show_country.html'


def permission_denied(request, *args, **kwargs):
    """
    Renders a custom 403 error page
    """
    return render(request, '403.html', status=403)


def page_not_found(request, *args, **kwargs):
    """
    Renders a custom 404 error page
    """
    return render(request, '404.html', status=404)


def server_error(request, *args, **kwargs):
    """
    Renders a custom 500 error page
    """
    return render(request, '500.html', status=500)
