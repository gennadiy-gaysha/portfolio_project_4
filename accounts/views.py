from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import RegisterForm


class RegisterNewAccount(CreateView):
    """
    A view for registering a new user account.

    Attributes:
    form_class: The form class used for creating a new user account. In this case,
    it is the UserCreationForm.
    template_name: The template used for rendering the registration form, here,
    'registration/register.html'.
    success_url: The URL to redirect to upon successful registration, specified
    using the reverse_lazy function and the 'login' URL name.
    """
    # form_class = UserCreationForm
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url =  reverse_lazy('login')
