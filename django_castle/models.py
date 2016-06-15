from django.contrib import auth, messages
from api import Castle
import inspect

__author__ = 'jens'

# Here we mainly define the signals to integrate into castle.io


def catch_login_signal(sender, request, user, **kwargs):
    castle = Castle()
    castle.log_login_success(user, request)
    messages.add_message(request, messages.INFO, inspect.stack(), extra_tags='alert-danger')

auth.signals.user_logged_in.connect(catch_login_signal, dispatch_uid="castle_login_signal")


def catch_logout_signal(sender, request, user, **kwargs):
    castle = Castle()
    castle.log_logout_success(user, request)
    messages.add_message(request, messages.INFO, inspect.stack(), extra_tags='alert-danger')

auth.signals.user_logged_out.connect(catch_logout_signal, dispatch_uid="castle_logout_signal")


def catch_loginfail_signal(request, **kwargs):
    user = request.POST.get('username', None)
    castle = Castle()
    castle.log_login_fail(user, request)
    messages.add_message(request, messages.INFO, inspect.stack(), extra_tags='alert-danger')

auth.signals.user_login_failed.connect(catch_loginfail_signal, dispatch_uid="castle_loginfail_signal")
