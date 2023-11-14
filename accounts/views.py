from django.contrib import messages
from django.contrib.auth import user_logged_in, user_logged_out
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import RegisterForm, EditDetailsForm, ChangePasswordForm, UserProfileForm
from accounts.models import UserProfile
from blog.models import Post


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

    def form_valid(self, form):
        messages.success(self.request, 'Account registered successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Error in {field}: {error}')
                return super().form_invalid(form)


def login_success(sender, request, user, **kwargs):
    messages.success(request, 'You have been logged in successfully.')


def logout_success(sender, request, user, **kwargs):
    messages.success(request, 'You have been logged out successfully.')


user_logged_in.connect(login_success)
user_logged_out.connect(logout_success)


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

    def form_valid(self, form):
        messages.success(self.request, 'Details have been updated successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Error in {field}: {error}')
                return super().form_invalid(form)


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

    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully.')
        return super().form_valid(form)


def author_bio(request, author_name):
    """
    Gets the User and UserProfile objects based on author name.

    Renders the author_bio.html template
    """
    author = User.objects.get(username=author_name)
    userprofile = UserProfile.objects.get(user=author)

    post_list = Post.objects.filter(author=author)

    return render(request, 'registration/author_bio.html',
                  {'author': author, 'userprofile': userprofile, 'post_list': post_list})


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
        messages.success(self.request, 'Profile created successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Error in {field}: {error}')
                return super().form_invalid(form)


class UpdateProfile(generic.UpdateView):
    """
    A class-based view for updating user profiles.

    Attributes:
    model: The model associated with the view, UserProfile, which determines the model
    the view interacts with.
    form_class: The form class associated with the view, UserProfileForm, which specifies
    the form used for updating user profiles.
    template_name: The name of the template used for rendering the update profile page,
    set to 'registration/update_profile.html'.

    Methods:
    get_object: Retrieves UserProfile object based on the username provided in the URL.
    """
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'registration/update_profile.html'

    def get(self, request, *args, **qwargs):
        userprofile = self.get_object()
        # Checks if the user is authenticated and has the permission to
        # change the post
        if not request.user.is_authenticated or not request.user == \
                                                    userprofile.user:
            raise PermissionDenied # Triggers permission_denied view
        return super().get(request, *args, **qwargs)

    def get_object(self, queryset=None):
        # this line extracts the username from the URL
        username = self.kwargs['username']
        # this line retrieves the User object with the specified username;
        # if a user with that username is not found, a 404 error is raised.
        user = get_object_or_404(User, username=username)
        # returns the associated userprofile by accessing it through the
        # user object. The UserProfile model is linked to the User model
        # via a OneToOneField. So, we can access the associated profile
        # through user.userprofile
        return user.userprofile

    def form_valid(self, form):

        form.instance.user = self.request.user
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Error in {field}: {error}')
                return super().form_invalid(form)
