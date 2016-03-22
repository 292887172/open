# -*- coding: utf-8 -*-

import inspect

from django.contrib.auth import get_backends, user_login_failed, _clean_credentials, get_user_model
from django.core.exceptions import PermissionDenied


def get_auth_user(**credentials):
    """
    不需要密码的验证
    """
    for backend in get_backends():
        try:
            inspect.getcallargs(backend.authenticate, **credentials)
        except TypeError:
            continue

        try:
            UserModel = get_user_model()
            user = UserModel._default_manager.get_by_natural_key(**credentials)
        except PermissionDenied:
            return None
        if user is None:
            continue
        user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
        return user
    user_login_failed.send(sender=__name__,
                           credentials=_clean_credentials(credentials))