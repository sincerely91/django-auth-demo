# -*- coding: utf-8
from django.contrib.auth import login
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.views.generic import FormView
from django.contrib.auth import logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.functional import lazy

from .forms import (AllAuthenticationForm,
                    MeAllAuthenticationForm, 
                    EmailUserCreationForm, 
                    ChangeEmailForm, ChangePasswordForm)
from . import signals
from . import app_settings


class RedirectMixin(object):
    redirect_field_name = REDIRECT_FIELD_NAME
    
    def get_success_url(self, default=None):
        """
        Redirect the user.
    
        :return: String containing the URI to redirect to.  
        """
        url = None
        
        if hasattr(self, 'redirect_field_name'):
            url = self.request.REQUEST.get(self.redirect_field_name, None)
        
        if not url and self.success_url:
            url = self.success_url

        if not url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")

        return url


class RequestMixin(FormView):
    def get_form_kwargs(self):
        kwargs = super(RequestMixin, self).get_form_kwargs()
        kwargs.update(request=self.request)
        return kwargs


class LoginView(RedirectMixin, RequestMixin, FormView):
    """
    Inspired by django.contrib.auth.views.login
    """
    template_name = "better/auth/login.html"
    form_class = AllAuthenticationForm
    success_url = settings.LOGIN_REDIRECT_URL

    def get_form(self, form_class):
        self.request.session.set_test_cookie()
        return super(LoginView, self).get_form(form_class)
    
    def form_valid(self, form):
        login(self.request, form.get_user())
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        
        if app_settings.AUTH_USE_MESSAGES:
            messages.success(self.request, _('You have been signed in.'),
                             fail_silently=True)
        
        return HttpResponseRedirect(self.get_success_url())


class MeLoginView(LoginView):
    form_class = MeAllAuthenticationForm
    
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me', None)

        if remember_me:
            self.request.session.set_expiry(app_settings.AUTH_REMEMBER_ME_DAYS * 24*60*60)
        else: 
            self.request.session.set_expiry(0)
            
        return super(MeLoginView, self).form_valid(form)


class SignupView(RedirectMixin, FormView):
    template_name = "better/auth/signup.html"
    form_class = EmailUserCreationForm
    success_url = app_settings.AUTH_SIGNUP_REDIRECT_URL
    is_active = False
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = self.is_active
        user.save()

        # Send the signup complete signal
        signals.signup_complete.send(sender=None, user=user)

        # A new signed user should logout the old one.
        if self.request.user.is_authenticated():
            logout(self.request)
        
        return HttpResponseRedirect(self.get_success_url())


class ChangeEmailView(RedirectMixin, RequestMixin, FormView):
    template_name = "better/auth/email_form.html"
    form_class = ChangeEmailForm
    success_url = lazy(reverse, str)('change_email_done')
    update_user = False
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        
        if self.update_user:
            self.request.user.email = email
            self.request.user.save()
            
        signals.email_complete.send(sender=None, 
                                    user=self.request.user, 
                                    email=email)

        return HttpResponseRedirect(self.get_success_url())


class ChangePasswordView(RedirectMixin, RequestMixin, FormView):
    template_name = "better/auth/password_form.html"
    form_class = ChangePasswordForm
    success_url = lazy(reverse, str)('change_password_done')
    update_user = True
    
    def form_valid(self, form):
        password = form.cleaned_data['password1']
        
        if self.update_user:
            self.request.user.set_password(password)
            self.request.user.save()
        
        """
        # TODO: 
        signals.password_complete.send(sender=None, 
                                    user=self.request.user, 
                                    password=password)
        """
        return HttpResponseRedirect(self.get_success_url())
   

signup_view = SignupView.as_view()
login_view = csrf_protect(never_cache(MeLoginView.as_view()))
change_email_view = csrf_protect(login_required(ChangeEmailView.as_view()))
change_password_view = csrf_protect(login_required(ChangePasswordView.as_view()))
