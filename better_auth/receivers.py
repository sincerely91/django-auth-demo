from django.dispatch import receiver
from better_emails.signals import confirmed
from better_emails.models import Address

@receiver(confirmed, sender=None)
def confirmed_handler(sender, operation, address, **kwargs):
    """
    * the user signs up
    * better_emails is notified
    * the user receives activation email
    * click the link, activate the email, notify the better_auth app
    """
    if operation=='signup':
        Address.objects.activate_user(address)
    elif operation=='email':
        Address.objects.set_primary(address)
