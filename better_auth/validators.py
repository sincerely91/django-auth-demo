from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from . import app_settings

class UniqueEmailValidator(object):
    user = None
    message_own = _(u'You\'re already known under this email.')
    code_own = 'own_email'
    message_exists = _(u'This email is already in use. Please supply a different email.')
    code_exists = 'exists_email'

    def __init__(self, user=None):
        if user is not None:
            self.user = user

    def __call__(self, value):
        """
        Validates that the input matches the regular expression.
        """
        exists_qs = User.objects.filter(email__iexact=value)
        if self.user:
            if value.lower() == self.user.email:
                raise ValidationError(self.message_own, code=self.code_own)

            if exists_qs.exclude(email__iexact=self.user.email).exists():
                raise ValidationError(self.message_exists, code=self.code_exists)
        else:
            if exists_qs.exists():
                raise ValidationError(self.message_exists, code=self.code_exists)


class ForbiddenUsernameValidator(object):
    code = 'forbidden_username'
    message = _(u'This username is not allowed.')
    
    def __init__(self):
        pass
    
    def __call__(self, value):
        if value.lower() in app_settings.AUTH_FORBIDDEN_USERNAMES:
            raise ValidationError(self.message, code=self.code)


class CurrentPasswordValidator(object):
    user = None
    code = 'bad_password'
    message = _(u'This is not the current password.')
    
    def __init__(self, user=None):
        if user is not None:
            self.user = user
    
    def __call__(self, value):
        if not self.user.check_password(value):
            raise ValidationError(self.message, code=self.code)