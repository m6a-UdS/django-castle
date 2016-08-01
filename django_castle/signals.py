import django.dispatch

registration_success_signal = django.dispatch.Signal(providing_args=["request", "enable_logging"])
registration_failed_signal = django.dispatch.Signal(providing_args=["request", "enable_logging"])
email_change_success_signal = django.dispatch.Signal(providing_args=["request", "enable_logging"])
email_change_requested_signal = django.dispatch.Signal(providing_args=["request", "enable_logging"])
email_change_failed_signal = django.dispatch.Signal(providing_args=["request", "enable_logging"])
password_reset_requested_signal = django.dispatch.Signal(providing_args=["request", "enable_logging"])
password_reset_failed_signal = django.dispatch.Signal(providing_args=["request", "enable_logging"])
password_reset_success_signal = django.dispatch.Signal(providing_args=["request", "enable_logging"])
password_change_failed_signal = django.dispatch.Signal(providing_args=["request", "enable_logging"])
password_change_success_signal = django.dispatch.Signal(providing_args=["request", "enable_logging"])
challenge_requested_signal = django.dispatch.Signal(providing_args=["request", "enable_logging"])
challenge_success_signal = django.dispatch.Signal(providing_args=["request", "enable_logging"])
challenge_failed_signal = django.dispatch.Signal(providing_args=["request", "enable_logging"])

# *** CUSTOM EVENTS *** #
login_ratelimited_signal = django.dispatch.Signal(providing_args=["request", "enable_logging"])
