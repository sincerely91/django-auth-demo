from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django.http import HttpRequest
from django.utils.importlib import import_module
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm 
from .validators import (
    UniqueEmailValidator, 
    CurrentPasswordValidator
)
from . import app_settings

fields = import_module(app_settings.AUTH_FIELDS_MODULE)

class UserAuthenticationForm(AuthenticationForm):
    """
    Show a login form with the following fields: (text) username, (text) password
    """
    username = forms.RegexField(**fields.username)
    password = forms.CharField(**fields.password)
    
    def get_messages(self, **kwargs):
        messages = {
            'incorrect': _("Please enter a correct username and password. Note that both fields are case-sensitive."),
            'inactive': _("This account is inactive.")
        }
        messages.update(kwargs)
        return messages
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(self.get_messages()['incorrect'])
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.get_messages()['inactive'])
        self.check_for_test_cookie()
        return self.cleaned_data


class AllAuthenticationForm(UserAuthenticationForm):
    """
    Show a login form with the following fields: (text) identification (username or email), (text) password
    """
    username = forms.CharField(**fields.identification)
    
    def get_messages(self):
        return super(AllAuthenticationForm, self).get_messages(
                   incorrect=_("Please enter a correct identifier (username or email) \
                                and a password. Note that both fields are case-sensitive."))


class MeMixin(forms.Form):
    remember_me = forms.BooleanField(**fields.rememberme)
    
    def __init__(self, request=None, *args, **kwargs):
        super(MeMixin, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['username', 'password', 'remember_me']
        
    
class MeUserAuthenticationForm(MeMixin, UserAuthenticationForm):
    """
    Show a login form with the following fields: (text) username, (text) password, (checkbox) remember me
    """
    pass


class MeAllAuthenticationForm(MeMixin, AllAuthenticationForm):
    pass


class EmailUserCreationForm(UserCreationForm):
    username = forms.RegexField(**fields.username)
    email = forms.EmailField(**dict(fields.email, validators=[UniqueEmailValidator()]))
    password1 = forms.CharField(**fields.password_new)
    password2 = forms.CharField(**fields.password_confirm)

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'email', 'password1', 'password2']


class BaseChangeForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        """
        The current ``user`` is needed for initialisation of this form so
        that we can check if the email address is still free and not always
        returning ``True`` for this query because it's the users own e-mail
        address.
        """
        if not isinstance(request, HttpRequest):
            raise TypeError, _("user must be an instance of User")
        else:
            self.request = request
        super(BaseChangeForm, self).__init__(*args, **kwargs)
    
    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        CurrentPasswordValidator(self.request.user)(current_password)
        return current_password
    
    def clean(self):
        if not self.request.user.is_authenticated():
            raise forms.ValidationError(_(u'You must be authenticated.'))
        return self.cleaned_data


class ChangeEmailForm(BaseChangeForm):
    current_password = forms.CharField(**fields.password_current)
    email = forms.EmailField(**fields.email_new)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        UniqueEmailValidator(self.request.user)(email)
        return email


class ChangePasswordForm(BaseChangeForm):
    current_password = forms.CharField(**fields.password_current)
    password1 = forms.CharField(**fields.password_new)
    password2 = forms.CharField(**fields.password_confirm)
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2