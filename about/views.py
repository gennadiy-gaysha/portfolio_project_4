from django.shortcuts import render
from about.models import About


def display_last_about(request):
    """
    Display the last 'About' instance on the about page.
    Args: request (HttpRequest): The HTTP request object.
    Returns (HttpResponse): The rendered about page containing the last
    'About' instance.
    """
    last_about = About.objects.last()
    context = {'last_about': last_about}
    return render(request, 'about/about_page.html', context)
