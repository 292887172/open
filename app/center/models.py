# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.crypto import salted_hmac
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib import auth
from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable)
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import python_2_unicode_compatible


class BaseUserManager(models.Manager):

    def __init__(self):
        self.model = None

    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the address by lowercasing the domain part of the email
        address.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email
    
    @classmethod
    def normalize_account(cls, account):
        """
        Normalize the address by lowercasing the domain part of the email
        address.
        """
        account = account or ''
        try:
            email_name, domain_part = account.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            account = '@'.join([email_name, domain_part.lower()])
        return account

    def make_random_password(self, length=10,
                             allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                           'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                           '23456789'):
        """
        Generates a random password with the given length and given
        allowed_chars. Note that the default value of allowed_chars does not
        have "I" or "O" or letters and digits that look similar -- just to
        avoid confusion.
        """
        return get_random_string(length, allowed_chars)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


@python_2_unicode_compatible
class AbstractBaseUser(models.Model):
    password = models.CharField(_('password'), max_length=512, db_column='ebf_account_password')
    last_login = models.DateTimeField(_('last login'), default=timezone.now, db_column="ebf_account_last_login")

    is_active = True

    REQUIRED_FIELDS = []

    class Meta:
        abstract = True

    def get_username(self):
        "Return the identifying username for this User"
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return self.get_username()

    def natural_key(self):
        return (self.get_username(),)

    def is_anonymous(self):
        """
        Always returns False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):

        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            pass
            # self.set_password(raw_password)
            #self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Sets a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        return is_password_usable(self.password)

    def get_full_name(self):
        raise NotImplementedError('subclasses of AbstractBaseUser must provide a get_full_name() method')

    def get_short_name(self):
        raise NotImplementedError('subclasses of AbstractBaseUser must provide a get_short_name() method.')

    def get_session_auth_hash(self):
        """
        Returns an HMAC of the password field.
        """
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.password).hexdigest()


# A few helper functions for common logic between User and AnonymousUser.
def _user_get_all_permissions(user, obj):
    permissions = set()
    for backend in auth.get_backends():
        if hasattr(backend, "get_all_permissions"):
            permissions.update(backend.get_all_permissions(user, obj))
    return permissions


def _user_has_perm(user, perm, obj):
    for backend in auth.get_backends():
        if hasattr(backend, "has_perm"):
            if backend.has_perm(user, perm, obj):
                return True
    return False


def _user_has_module_perms(user, app_label):
    for backend in auth.get_backends():
        if hasattr(backend, "has_module_perms"):
            if backend.has_module_perms(user, app_label):
                return True
    return False