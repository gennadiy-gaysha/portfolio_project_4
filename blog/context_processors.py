from blog.models import Post


def draft_posts(request):
    """
     Retrieves the number of posts currently under moderation for the logged-in user.

    Args:
    - request: The request object associated with the current HTTP request.

    Returns:
    A dictionary containing the number of posts on moderation as a context variable.
    The number is obtained by filtering the Post model based on the author being the logged-in user
    and the status being 1 (indicating moderation).

    If the user is not authenticated, the number of posts on moderation is set to 0.
    """
    # assign the current user from the request to the variable user
    user = request.user
    if user.is_authenticated:
        num_draft_posts = Post.objects.filter(author=user, status=0).count()
    else:
        num_draft_posts = 0
    return {'num_draft_posts': num_draft_posts}


def moderated_posts(request):
    user = request.user
    if user.is_authenticated:
        num_moderated_posts = Post.objects.filter(author=user, status=1).count()
    else:
        num_moderated_posts = 0
    return {'num_moderated_posts': num_moderated_posts}
