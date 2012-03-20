from . import app_settings
from .utils import import_object

patcher = import_object(app_settings.AUTH_PATCHER_OBJECT)
patcher().patch()