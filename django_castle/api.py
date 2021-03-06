import json
from django.conf import settings
from django.contrib import auth
from django_castle.utils import castle_userid
import requests
import pprint

from utils import logmessage


__author__ = 'jens'


class Castle(object):

    def __init__(self, api_secret=None, api_url=None, default_ip_header=None):
        self.LOGIN_SUCCESS = "$login.succeeded"
        self.LOGIN_FAILED = "$login.failed"
        self.LOGIN_RATELIMITED = "login.ratelimited"
        self.LOGOUT_SUCCEEDED = "$logout.succeeded"
        self.REGISTRATION_SUCCEEDED = "$registration.succeeded"
        self.REGISTRATION_FAILED = "$registration.failed"
        self.EMAIL_CHANGE_REQUESTED = "$email_change.requested"
        self.EMAIL_CHANGE_SUCCEEDED = "$email_change.succeeded"
        self.EMAIL_CHANGE_FAILED = "$email_change.failed"
        self.PASSWORD_RESET_REQUESTED = "$password_reset.requested"
        self.PASSWORD_RESET_SUCCEEDED = "$password_reset.succeeded"
        self.PASSWORD_RESET_FAILED = "$password_reset.failed"
        self.PASSWORD_CHANGE_SUCCEEDED = "$password_change.succeeded"
        self.PASSWORD_CHANGE_FAILED = "$password_change.failed"
        self.CHALLENGE_REQUESTED = "$challenge.requested"
        self.CHALLENGE_SUCCEEDED = "$challenge.succeeded"
        self.CHALLENGE_FAILED = "$challenge.failed"

        self.api_secret = ""
        self.api_url = ""
        self.default_ip_header = ""
        self.default_source = "backend"
        self.CASTLE_TIMEOUT = getattr(settings, "CASTLE_TIMEOUT", 10)

        if not api_url:
            api_url = getattr(settings, "CASTLE_API_URL", "https://api.castle.io/v1")
            self.api_url = api_url
        if not api_secret:
            api_secret = getattr(settings, "CASTLE_API_SECRET")
            self.api_secret = api_secret
        if not default_ip_header:
            default_ip_header = getattr(settings, "CASTLE_IP_HEADER", "REMOTE_ADDR")
            self.default_ip_header = default_ip_header

    def log_event(self, request, event, source=None, enable_logging=False):
        source = source if source else self.default_source
        headers = self.get_headers_from_request(request, source=source)
        user_id = castle_userid(request.user) if request else "<no-id>"
        resp = self.make_request("events", data={"name": event, "user_id": user_id}, headers=headers)
        if request and enable_logging:
            logmessage(request, pprint.pformat(resp))

    # ***
    # This event is a special case because we want to catch the credentials and no user is yet defined
    # ***
    def log_login_fail(self, credentials, source=None):
        source = source if source else self.default_source
        username = credentials.get("username", None)
        request = credentials.get("request", None)
        headers = self.get_headers_from_request(request, source=source)
        self.make_request("events", data={"name": self.LOGIN_FAILED, "details": {"$login": username}}, headers=headers)

    # ***
    # Specialised version of log_event; Kept for reverse-compatibility
    # ***
    def log_login_success(self, user, request):
        headers = self.get_headers_from_request(request)
        user_id = castle_userid(user) if user else "<no-id>"
        self.make_request("events", data={"name": "$login.succeeded", "user_id": user_id}, headers=headers)

    # ***
    # Specialised version of log_event; Kept for reverse-compatibility
    # ***
    def log_logout_success(self, user, request):
        headers = self.get_headers_from_request(request)
        user_id = castle_userid(user) if user else ""
        self.make_request("events", data={"name": "$logout.succeeded", "user_id": user_id}, headers=headers)

    def get_headers_from_request(self, request, ip_header=None, source=None):
        source = source if source else self.default_source
        ip_header = ip_header if ip_header else self.default_ip_header
        return {
            "X-Castle-Cookie-Id": request.COOKIES.get("__cid", "-"),
            "X-Castle-Ip": request.META.get(ip_header, '127.0.0.1'),
            "X-Castle-Headers": json.dumps({
                "User-Agent": request.META.get("HTTP_USER_AGENT", "NOT_PRESENT"),
                "Accept": request.META.get("HTTP_ACCEPT", "NOT_PRESENT"),
                "Accept-Encoding": request.META.get("HTTP_ACCEPT_ENCODING", "NOT_PRESENT"),
                "Accept-Language": request.META.get("HTTP_ACCEPT_LANGUAGE", "NOT_PRESENT"),
            }),
            "X-Castle-Source": source,
            "Content-Type": "application/json"
        } if request else {}

    def make_request(self, endpoint, data, headers):
        url = "%s/%s" % (self.api_url, endpoint)
        r = requests.post(url=url, data=json.dumps(data), headers=headers, auth=('', self.api_secret), timeout=self.CASTLE_TIMEOUT)
        return [url, str(r.status_code), r.text, r.headers, headers, data]
