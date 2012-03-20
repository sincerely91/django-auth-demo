from django.utils.importlib import import_module
from . import app_settings

if app_settings.AUTH_RECEIVERS_MODULE:
    import_module(app_settings.AUTH_RECEIVERS_MODULE)