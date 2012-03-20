from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from .views import login_view, signup_view, change_email_view, change_password_view
from .utils import import_object
from . import app_settings

class UrlBuilder(object):
    """
    TODO: build the metaclass
    """
    login =                     url(r'^login/$', login_view, name='login')
    signup =                    url(r'^signup/$', signup_view, name='signup')
    signup_done =               url(r'^signup_done/$', 
                                    TemplateView.as_view(template_name="better/auth/signup_done.html"),
                                    name='signup_done')
    logout =                    url(r'^logout/$', auth_views.logout, 
                                    {'next_page': app_settings.AUTH_LOGOUT_REDIRECT_URL,
                                     'template_name': 'better/auth/logout.html'},
                                    name='logout')
    change_email =              url(r'^change_email/$', change_email_view, 
                                    name='change_email')
    change_email_done =         url(r'^change_email_done/$', 
                                    TemplateView.as_view(template_name="better/auth/change_email_done.html"),
                                    name='change_email_done')
    change_password =           url(r'^change_password/$', change_password_view, 
                                    name='change_password')
    change_password_done =      url(r'^change_password_done/$', 
                                    TemplateView.as_view(template_name="better/auth/change_password_done.html"),
                                    name='change_password_done')
    password_reset =            url(r'^password/reset/$', auth_views.password_reset,
                                    {'template_name': 'better/auth/password_reset_form.html',
                                     'email_template_name': 'better/auth/emails/password_reset_message.txt'},
                                    name='password_reset')
    password_reset_done =       url(r'^password/reset/done/$', auth_views.password_reset_done,
                                    {'template_name': 'better/auth/password_reset_done.html'},
                                    name='password_reset_done')
    password_reset_confirm =    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                                    auth_views.password_reset_confirm,
                                    {'template_name': 'better/auth/password_reset_confirm_form.html'},
                                    name='password_reset_confirm')
    password_reset_complete =   url(r'^password/reset/confirm/complete/$',
                                    auth_views.password_reset_complete,
                                    {'template_name': 'better/auth/password_reset_complete.html'},
                                    name='password_reset_complete')
    

    def get_url_names(self):
        return ['login', 'signup', 'signup_done', 'logout',
                'change_email', 'change_email_done',
                'change_password', 'change_password_done', 
                'password_reset', 'password_reset_done', 
                'password_reset_confirm', 'password_reset_complete']
    
    @property
    def urls(self):
        return [getattr(self, url_name) for url_name in self.get_url_names()]


url_builder_class = import_object(app_settings.AUTH_URL_BUILDER_OBJECT)
urlpatterns = patterns('', *url_builder_class().urls)