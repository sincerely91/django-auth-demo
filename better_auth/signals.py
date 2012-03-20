from django.dispatch import Signal

signup_complete = Signal(providing_args=["user",])
email_complete = Signal(providing_args=["user", "email"])
