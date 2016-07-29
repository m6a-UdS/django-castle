import django.dispatch

registration_success_signal = django.dispatch.Signal(providing_args=["request"])
registration_failed_signal = django.dispatch.Signal(providing_args=["request"])
email_change_success_signal = django.dispatch.Signal(providing_args=["request"])
email_change_requested_signal = django.dispatch.Signal(providing_args=["request"])
email_change_failed_signal = django.dispatch.Signal(providing_args=["request"])
password_reset_requested_signal = django.dispatch.Signal(providing_args=["request"])
password_reset_failed_signal = django.dispatch.Signal(providing_args=["request"])
password_reset_success_signal = django.dispatch.Signal(providing_args=["request"])
password_change_failed_signal = django.dispatch.Signal(providing_args=["request"])
password_change_success_signal = django.dispatch.Signal(providing_args=["request"])
challenge_requested_signal = django.dispatch.Signal(providing_args=["request"])
challenge_success_signal = django.dispatch.Signal(providing_args=["request"])
challenge_failed_signal = django.dispatch.Signal(providing_args=["request"])

# *** CUSTOM EVENTS *** #
login_ratelimited_signal = django.dispatch.Signal(providing_args=["request"])
