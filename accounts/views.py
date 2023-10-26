from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import RegisterForm, EditDetailsForm, ChangePasswordForm, UserProfileForm
from accounts.models import UserProfile


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


class ChangePassword(PasswordChangeView):
    """
    A view for allowing users to change their passwords.

    Attributes:
    form_class: The form class used for changing the user's password, which is set to
    ChangePasswordForm.
    template_name: The name of the template used for rendering the change password page,
    set to 'registration/change_password.html'.
    success_url: The URL to redirect to upon successfully changing the password, utilizing
    the reverse_lazy method with the 'home' URL name.
    """
    form_class = ChangePasswordForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('home')


def author_bio(request, author_name):
    """
    Gets the User and UserProfile objects based on author name.

    Renders the author_bio.html template
    """
    author = User.objects.get(username=author_name)
    userprofile = UserProfile.objects.get(user=author)

    return render(request, 'registration/author_bio.html', {'author': author, 'userprofile': userprofile})



class CreateProfile(generic.CreateView):
    """
    A view that handles the creation of user profiles. The view utilizes the
    generic.CreateView class from Django to handle the form creation process and
    template rendering.

    Attributes:
    model: The model associated with the view, UserProfile, which determines the model
    the view interacts with.
    form_class: The form class associated with the view, UserProfileForm, which specifies
    the form used for creating and updating user profiles.
    template_name: The name of the template used for rendering the create profile page,
    set to 'registration/create_profile.html'
    """
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'registration/create_profile.html'

    def form_valid(self, form):
        """
        Setting the user field of the profile to the currently logged-in user
        """
        form.instance.user = self.request.user
        return super().form_valid(form)
