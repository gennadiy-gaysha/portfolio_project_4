from django.shortcuts import render
from about.models import About


def display_last_about(request):
    last_about = About.objects.last()
    context = {'last_about': last_about}
    return render(request, 'about/about_page.html', context)
