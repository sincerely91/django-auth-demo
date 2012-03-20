from django import forms
from django.utils.translation import ugettext_lazy as _
from .validators import UniqueEmailValidator, ForbiddenUsernameValidator
from . import app_settings

username = {
   'label': _(u"Username"),
   'regex': r'^[\w.@+-]+$',
   'min_length': 1,
   'max_length': 100,
   'error_messages': {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")},
   'help_text': _("Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only."),
   'validators': [ForbiddenUsernameValidator()]
}

email = {
    'label': _("Email"),
    'min_length': 5,
    'max_length': 100,
    'widget': forms.TextInput(attrs=dict(maxlength=100)),
}

identification = {
    'label': _(u"Email/Username"),
    'help_text': _(u"Either supply us with your email or username.")
}

rememberme = {
    'widget': forms.CheckboxInput(),
    'required': False,
    'label': _(u'Remember me for %(days)d days.') % {'days': app_settings.AUTH_REMEMBER_ME_DAYS}
}

email_new = dict(email, label=_("New Email"))

password = {
    'label': _("Password"), 
    'widget': forms.PasswordInput
}

password_current = dict(password, label=_("Current Password"))

password_new = dict(password, label=_("New Password"))

password_confirm = {
    'label': _("Password confirmation"),
    'widget': forms.PasswordInput,
    'help_text': _("Enter the same password as above, for verification.")
}
