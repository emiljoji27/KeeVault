from asyncio.windows_events import NULL
from pickle import FALSE
from django import forms
# from .models import PostsCreation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

from .models import PasswordModel
username_validator = UnicodeUsernameValidator()

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label=_('Username'),max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={'unique': _("Username already exists.")},
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Search'})
    )

    password1 = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': "form-control form-control-lg",'placeholder': 'Search'}))

    password2 = forms.CharField(label=_("Confirm Password"), widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': "form-control form-control-lg",'placeholder': 'Search'}), 
        strip=False, help_text=_("Enter the same password as before, for verification."))
    
    email = forms.EmailField(label=_('Email'), widget=forms.TextInput(
        attrs={'class': "form-control form-control-lg",'placeholder': 'Search'}))

    class Meta:
        model = User
        fields = ['email', 'username']


class PasswordEntryForm(forms.ModelForm):
    class Meta:
        model = PasswordModel
        fields = ['name','login_url','login_username','login_password']