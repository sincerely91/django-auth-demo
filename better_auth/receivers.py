from django.dispatch import receiver
from better.emails.signals import confirmed
from better.emails.models import Address

@receiver(confirmed, sender=None)
def confirmed_handler(sender, operation, address, **kwargs):
    """
    * the user signs up
    * better.emails is notified
    * the user receives activation email
    * click the link, activate the email, notify the better.auth
    """
    if operation=='signup':
        Address.objects.activate_user(address)
    elif operation=='email':
        Address.objects.set_primary(address)
