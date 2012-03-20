from django.core.exceptions import MultipleObjectsReturned
from django.core.validators import email_re
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class AuthenticationBackend(ModelBackend):
    """
    Custom backend because the user must be able to supply a ``email`` or
    ``username`` to the login form.

    """
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False
    
    def authenticate(self, username=None, password=None):
        """
        Authenticates a user through the combination email/username with
        password.

        :param identification:
            A string containing the username or e-mail of the user that is
            trying to authenticate.

        :password:
            Optional string containing the password for the user.

        :param check_password:
            Boolean that defines if the password should be checked for this
            user.  Always keep this ``True``. This is only used by userena at
            activation when a user opens a page with a secret hash.

        :return: The signed in :class:`User`.

        """
        if not (username and password):
            return None
        
        if email_re.search(username):
            try: 
                user = User.objects.get(email__iexact=username)
            except (User.DoesNotExist, MultipleObjectsReturned): 
                return None
        else:
            try: 
                user = User.objects.get(username__iexact=username)
            except (User.DoesNotExist, MultipleObjectsReturned):
                return None

        if user.check_password(password):
            return user
        else:
            return None
