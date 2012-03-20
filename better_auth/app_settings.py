from django.conf import settings

AUTH_REMEMBER_ME_DAYS = getattr(settings,
'AUTH_REMEMBER_ME_DAYS', 30)

AUTH_USE_MESSAGES = getattr(settings,
'AUTH_USE_MESSAGES', True)

AUTH_FORBIDDEN_USERNAMES = getattr(settings,
'AUTH_FORBIDDEN_USERNAMES', 
('admin', 'signup', 'signout', 'signin', 'activate', 'me', 'password'))

AUTH_SIGNUP_REDIRECT_URL = getattr(settings,
'AUTH_SIGNUP_REDIRECT_URL', "/")

AUTH_LOGOUT_REDIRECT_URL = getattr(settings,
'AUTH_LOGOUT_REDIRECT_URL', "/")

AUTH_PATCHER_OBJECT = getattr(settings,
'AUTH_PATCHER', "better.auth.patches.UserPatch") 

AUTH_URL_BUILDER_OBJECT = getattr(settings,
'AUTH_URL_BUILDER', "better.auth.urls.UrlBuilder")

AUTH_RECEIVERS_MODULE = getattr(settings,
'AUTH_RECEIVERS', "better.auth.receivers")

AUTH_FIELDS_MODULE = getattr(settings,
'AUTH_FIELDS', "better.auth.fields")