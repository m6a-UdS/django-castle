from django.contrib import auth
from api import Castle
from .signals import *

__author__ = 'jens'

# Here we mainly define the signals to integrate into castle.io


def catch_login_signal(sender, request, **kwargs):
    castle = Castle()
    castle.log_event(request, castle.LOGIN_SUCCESS, enable_logging=True)

auth.signals.user_logged_in.connect(catch_login_signal, dispatch_uid="castle_login_signal")


def catch_logout_signal(sender, request, **kwargs):
    castle = Castle()
    castle.log_event(request, castle.LOGOUT_SUCCEEDED, enable_logging=True)

auth.signals.user_logged_out.connect(catch_logout_signal, dispatch_uid="castle_logout_signal")


def catch_loginfail_signal(sender, credentials=None, **kwargs):
    castle = Castle()
    castle.log_login_fail(credentials)

auth.signals.user_login_failed.connect(catch_loginfail_signal, dispatch_uid="castle_loginfail_signal")


def catch_registration_success_signal(sender, request, **kwargs):
    castle = Castle()
    castle.log_event(request, castle.REGISTRATION_SUCCEEDED, enable_logging=True)

registration_success_signal.connect(catch_registration_success_signal, dispatch_uid="registration_success_signal")


def catch_registration_failed_signal(sender, request, **kwargs):
    castle = Castle()
    castle.log_event(request, castle.REGISTRATION_FAILED, enable_logging=True)

registration_failed_signal.connect(catch_registration_failed_signal, dispatch_uid="registration_failed_signal")


def catch_email_change_request_signal(sender, request, **kwargs):
    castle = Castle()
    castle.log_event(request, castle.EMAIL_CHANGE_REQUESTED, enable_logging=True)

email_change_requested_signal.connect(catch_email_change_request_signal, dispatch_uid="email_change_requested_signal")


def catch_email_change_failed_signal(sender, request, **kwargs):
    castle = Castle()
    castle.log_event(request, castle.EMAIL_CHANGE_FAILED, enable_logging=True)

email_change_failed_signal.connect(catch_email_change_failed_signal, dispatch_uid="email_change_failed_signal")


def catch_email_change_success_signal(sender, request, **kwargs):
    castle = Castle()
    castle.log_event(request, castle.EMAIL_CHANGE_SUCCEEDED, enable_logging=True)

email_change_success_signal.connect(catch_email_change_success_signal, dispatch_uid="email_change_success_signal")


def catch_password_reset_requested_signal(sender, request, **kwargs):
    castle = Castle()
    castle.log_event(request, castle.PASSWORD_RESET_REQUESTED, enable_logging=True)

password_reset_requested_signal.connect(catch_password_reset_requested_signal, dispatch_uid="password_reset_requested_signal")


def catch_password_reset_failed_signal(sender, request, **kwargs):
    castle = Castle()
    castle.log_event(request, castle.PASSWORD_RESET_FAILED, enable_logging=True)

password_reset_failed_signal.connect(catch_password_reset_failed_signal, dispatch_uid="password_reset_failed_signal")


def catch_password_reset_success_signal(sender, request, **kwargs):
    castle = Castle()
    castle.log_event(request, castle.EMAIL_CHANGE_FAILED, enable_logging=True)

password_reset_success_signal.connect(catch_password_reset_success_signal, dispatch_uid="password_reset_success_signal")


def catch_password_change_failed_signal(sender, request, **kwargs):
    castle = Castle()
    castle.log_event(request, castle.PASSWORD_CHANGE_FAILED, enable_logging=True)

password_change_failed_signal.connect(catch_password_change_failed_signal, dispatch_uid="password_change_failed_signal")


def catch_password_change_success_signal(sender, request, **kwargs):
    castle = Castle()
    castle.log_event(request, castle.PASSWORD_CHANGE_SUCCEEDED, enable_logging=True)

password_change_success_signal.connect(catch_password_change_success_signal, dispatch_uid="password_change_success_signal")


def catch_challenge_requested_signal(sender, request, **kwargs):
    castle = Castle()
    castle.log_event(request, castle.CHALLENGE_REQUESTED, enable_logging=True)

challenge_requested_signal.connect(catch_challenge_requested_signal, dispatch_uid="challenge_requested_signal")


def catch_challenge_failed_signal(sender, request, **kwargs):
    castle = Castle()
    castle.log_event(request, castle.CHALLENGE_FAILED, enable_logging=True)

challenge_failed_signal.connect(catch_challenge_failed_signal, dispatch_uid="challenge_failed_signal")


def catch_challenge_success_signal(sender, request, **kwargs):
    castle = Castle()
    castle.log_event(request, castle.CHALLENGE_SUCCEEDED, enable_logging=True)

challenge_success_signal.connect(catch_challenge_success_signal, dispatch_uid="challenge_success_signal")
