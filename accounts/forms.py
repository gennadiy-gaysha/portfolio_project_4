from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, \
    PasswordChangeForm
from django.contrib.auth.models import User
from django_summernote.widgets import SummernoteWidget

from accounts.models import UserProfile
from blog.models import Country


class RegisterForm(UserCreationForm):
    """
    A form used for registering new users. Inherits from UserCreationForm.

    Attributes:
    username: A char field for the username with a maximum length of 20
    characters and a 'form-control' widget.
    first_name: A char field for the first name with a maximum length of 50
    characters and a 'form-control' widget.
    last_name: A char field for the last name with a maximum length of 50
    characters and a 'form-control' widget.
    email: An email field for the email address with a maximum length of 50
    characters and a 'form-control error-message' widget.

    Methods:
    clean_email: A method that cleans the email field and checks if the email
    already exists in the User model. Raises a validation error if the email
    already exists.
    """
    username = forms.CharField(
        widget=forms.TextInput({'class': 'form-control'}), max_length=20)
    first_name = forms.CharField(
        widget=forms.TextInput({'class': 'form-control'}), max_length=50)
    last_name = forms.CharField(
        widget=forms.TextInput({'class': 'form-control'}), max_length=50)
    email = forms.EmailField(
        widget=forms.EmailInput({'class': 'form-control error-message'}),
        max_length=50)

    def clean_email(self):
        """
        Cleans the email field and checks if the email already exists in the
        User model. Raises a validation error if the email already exists.
        """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'This email address is already in use.')
        return email

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1',
                  'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields[
            'password1'].help_text = "* Your password can’t be too similar " \
                                     "to your other personal information." \
                                     "<br>* Your password must contain at " \
                                     "least 8 characters.<br>* Your " \
                                     "password can’t be a commonly used " \
                                     "#password.<br>* Your password can’t " \
                                     "be entirely numeric."
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields[
            'username'].help_text = '<span>*Required. 20 characters or ' \
                                    'fewer. Letters, digits and @/./+/-/_ ' \
                                    'only.</span><br><span style="color: ' \
                                    'green">*Disclaimer: ' \
                                    'Once created, you cannot change your ' \
                                    'username.</span>'


class EditDetailsForm(UserChangeForm):
    first_name = forms.CharField(
        widget=forms.TextInput({'class': 'form-control'}), max_length=50)
    last_name = forms.CharField(
        widget=forms.TextInput({'class': 'form-control'}), max_length=50)
    email = forms.EmailField(
        widget=forms.EmailInput({'class': 'form-control'}), max_length=50)
    last_login = forms.CharField(
        widget=forms.TextInput({'class': 'form-control', 'readonly': True}),
        max_length=50)
    date_joined = forms.CharField(
        widget=forms.TextInput({'class': 'form-control', 'readonly': True}),
        max_length=50)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'last_login',
                  'date_joined']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'readonly': True})
        self.fields[
            'username'].help_text = '<span style="color: green">Disclaimer: ' \
                                    'Once created, you cannot change your ' \
                                    'username.</span>'


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control'})


class UserProfileForm(forms.ModelForm):
    """
    A form used for creating and updating user profiles. Additionally, the
    widget attribute customizes the appearance and behavior of the form fields,
    such as defining the ty pe of input for each field along with associated
    attributes for controlling their presentation.
    Attributes:
    model: The model associated with the form, in this case, the UserProfile
    model. fields: A tuple indicating the specific fields from the UserProfile
    model to b included in the form.
    widgets: A dictionary containing the various widget attributes for each
    form field
    Methods:
    __init__: Initializes the form, setting up the help text for the
    'date_of_birth' field, providing instructions for the expected date
    format. The super function is called, which refers to the superclass and
    initializes the form with any additional arguments passed to it.
    """
    home_country = forms.ModelChoiceField(
        queryset=Country.objects.all().order_by('country_name'),
        widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = UserProfile
        fields = (
            'profile_picture', 'bio', 'home_country', 'gender',
            'date_of_birth',
            'instagram_profile', 'twitter_profile', 'facebook_profile',
            'linkedin_profile')

        widgets = {
            'profile_picture': forms.FileInput(
                attrs={'class': 'form-control-file'}),
            'bio': SummernoteWidget(),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(
                attrs={'class': 'form-control', 'id': 'datepicker',
                       'name': 'date_of_birth'}),
            'instagram_profile': forms.URLInput(
                attrs={'class': 'form-control'}),
            'twitter_profile': forms.URLInput(attrs={'class': 'form-control'}),
            'facebook_profile': forms.URLInput(
                attrs={'class': 'form-control'}),
            'linkedin_profile': forms.URLInput(
                attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            'date_of_birth'].help_text = '<span style="color: green;">' \
                                         'YYYY-MM-DD ' \
                                         '(please, follow this date format)' \
                                         '</span>'
