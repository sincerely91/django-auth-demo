import sys
import re
from django.contrib.auth.models import User
from django.utils.importlib import import_module
from . import app_settings

fields = import_module(app_settings.AUTH_FIELDS_MODULE)

class UserPatch(object):
    user_model = User
    
    def get_field(self, name):
        return getattr(self.user_model, '_meta').get_field_by_name(name)[0]
        
    def patch_email(self):
        email = self.get_field('email')
        email._unique = True
        email.blank = False
        for key, value in fields.email.items():
            setattr(email, key, value) 
    
    def patch_username(self):
        username = self.get_field('username')
        for key, value in fields.username.items():
            setattr(username, key, value)
    
    def patch_groups(self):
        groups = self.get_field('groups')
        groups.blank = False
    
    def add_fields(self, fields):
        """
        fields is a dictionary
        """
        for field_name, field_obj in fields.items():
            getattr(self.user_model, 'add_to_class')(field_name, field_obj)
    
    def delete_fields(self, fields):
        """
        fields is a list of field names
        """
        self.user_model._meta.local_fields = filter(lambda field: field.name not in fields, 
                                             getattr(User, '_meta').local_fields)
    
    def add_create_username(self):
        @staticmethod
        def create_username(email):
            return re.sub(r"[^\w]+", ".", email.split('@')[0]) if email else None
        getattr(self.user_model, 'add_to_class')("create_username", create_username)
    
    def patch_save(self):
        self.add_create_username()
        
        def save(myself, *args, **kwargs):
            # create the username if it's an insert op and username is empty
            if not myself.pk and not myself.username:
                myself.username = getattr(User, 'create_username')(myself.email)
            return super(self.user_model, myself).save(*args, **kwargs)
        getattr(self.user_model, 'add_to_class')("save", save)
    
    def patch_get_absolute_url(self):
        delattr(self.user_model, 'get_absolute_url')
        #def get_absolute_url(self):
        #    return "/users/%s/" % urllib.quote(smart_str(self.username))

    def patch(self):
        self.patch_email()
        self.patch_username()
        self.patch_save()