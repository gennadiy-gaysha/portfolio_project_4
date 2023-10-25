from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import RegisterForm, EditDetailsForm


class RegisterNewAccount(generic.CreateView):
    """
    A view for registering a new user account.

    Attributes:
    form_class: The form used for user registration, which in this case is the
    RegisterForm.
    template_name: The template used for rendering the registration form, here,
    'registration/register.html'.
    success_url: The URL to redirect to upon successful registration, specified
    using the reverse_lazy function and the 'login' URL name.
    """
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class EditDetails(generic.UpdateView):
    """
    A view for editing user registration details.

    Attributes:
    form_class: The form class used for updating user details, which is set to
    UserChangeForm.
    template_name: The name of the template used for rendering the user details edit
    page, set to 'registration/edit_details.html'.
    success_url: The URL to redirect to upon successfully updating the user details,
    utilizing the reverse_lazy method.
    """
    form_class = EditDetailsForm
    template_name = 'registration/edit_details.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        """
        Retrieves the current logged-in user.

        Returns:
        The user object representing the currently logged-in user.
        """
        return self.request.user
