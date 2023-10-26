from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


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

    def __init__(self, *args, **qwargs):
        super().__init__(*args, **qwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields[
            'username'].help_text = '<span style="color: green">Disclaimer: Once ' \
            'created, you cannot change your username.</span><br><span>Required. ' \
            '20 characters or fewer. Letters, digits and @/./+/-/_ only.</span>'


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

    def __init__(self, *args, **qwargs):
        super().__init__(*args, **qwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'readonly': True})
        self.fields[
            'username'].help_text = '<span style="color: green">Disclaimer: Once ' \
            'created, you cannot change your username.</span>'
