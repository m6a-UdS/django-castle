import json
from django.conf import settings
from utils import castle_userid
import requests

__author__ = 'jens'

CASTLE_TIMEOUT = getattr(settings, "CASTLE_TIMEOUT", 10)


class Castle(object):
    api_secret = ""
    api_url = ""

    def __init__(self, api_secret=None, api_url=None):
        if not api_url:
            api_url = getattr(settings, "CASTLE_API_URL", "https://api.castle.io/v1")
            self.api_url = api_url
        if not api_secret:
            api_secret = getattr(settings, "CASTLE_API_SECRET")
            self.api_secret = api_secret

    def log_login_success(self, user, request):
        headers = self.get_headers_from_request(request, ip_header="HTTP_X_REAL_IP")
        user_id = castle_userid(user) if user else ""
        self.make_request("events", data={"name": "$login.succeeded", "user_id": user_id}, headers=headers)

    def log_login_fail(self, credentials):
        username = credentials.get("username", None)
        request = credentials.get("request", None)
        headers = self.get_headers_from_request(request, ip_header="HTTP_X_REAL_IP")
        self.make_request("events", data={"name": "$login.failed", "details": {"$login": username}}, headers=headers)

    def log_logout_success(self, user, request):
        headers = self.get_headers_from_request(request, ip_header="HTTP_X_REAL_IP")
        user_id = castle_userid(user) if user else ""
        self.make_request("events", data={"name": "$logout.succeeded", "user_id": user_id}, headers=headers)

    def log_user_registration_success(self, request):
        headers = self.get_headers_from_request(request, source="backend", ip_header="HTTP_X_REAL_IP")
        user_id = castle_userid(request.user) if request.user else ""
        self.make_request("events", data={"name": "$registration.succeeded", "user_id": user_id}, headers=headers)

    def log_user_registration_failed(self, request):
        headers = self.get_headers_from_request(request, source="backend", ip_header="HTTP_X_REAL_IP")
        user_id = castle_userid(request.user) if request.user else ""
        self.make_request("events", data={"name": "$registration.failed", "user_id": user_id}, headers=headers)

    def log_email_change_request(self, request):
        headers = self.get_headers_from_request(request, source="backend", ip_header="HTTP_X_REAL_IP")
        user_id = castle_userid(request.user) if request.user else ""
        self.make_request("events", data={"name": "$email_change.requested", "user_id": user_id}, headers=headers)

    def log_email_change_success(self, request):
        headers = self.get_headers_from_request(request, source="backend", ip_header="HTTP_X_REAL_IP")
        user_id = castle_userid(request.user) if request.user else ""
        self.make_request("events", data={"name": "$email_change.succeeded", "user_id": user_id}, headers=headers)

    def log_email_change_failed(self, request):
        headers = self.get_headers_from_request(request, source="backend", ip_header="HTTP_X_REAL_IP")
        user_id = castle_userid(request.user) if request.user else ""
        self.make_request("events", data={"name": "$email_change.failed", "user_id": user_id}, headers=headers)

    def log_password_reset_requested(self, request):
        headers = self.get_headers_from_request(request, source="backend", ip_header="HTTP_X_REAL_IP")
        user_id = castle_userid(request.user) if request.user else ""
        self.make_request("events", data={"name": "$password_reset.requested", "user_id": user_id}, headers=headers)

    def log_password_reset_success(self, request):
        headers = self.get_headers_from_request(request, source="backend", ip_header="HTTP_X_REAL_IP")
        user_id = castle_userid(request.user) if request.user else ""
        self.make_request("events", data={"name": "$password_reset.succeeded", "user_id": user_id}, headers=headers)

    def log_password_reset_failed(self, request):
        headers = self.get_headers_from_request(request, source="backend", ip_header="HTTP_X_REAL_IP")
        user_id = castle_userid(request.user) if request.user else ""
        self.make_request("events", data={"name": "$password_change.failed", "user_id": user_id}, headers=headers)

    def log_password_change_success(self, request):
        headers = self.get_headers_from_request(request, source="backend", ip_header="HTTP_X_REAL_IP")
        user_id = castle_userid(request.user) if request.user else ""
        self.make_request("events", data={"name": "$password_change.succeeded", "user_id": user_id}, headers=headers)

    def log_password_change_fail(self, request):
        headers = self.get_headers_from_request(request, source="backend", ip_header="HTTP_X_REAL_IP")
        user_id = castle_userid(request.user) if request.user else ""
        self.make_request("events", data={"name": "$password_change.failed", "user_id": user_id}, headers=headers)

    def log_challenge_requested(self, request):
        headers = self.get_headers_from_request(request, source="backend", ip_header="HTTP_X_REAL_IP")
        user_id = castle_userid(request.user) if request.user else ""
        self.make_request("events", data={"name": "$challenge.requested", "user_id": user_id}, headers=headers)

    def log_challenge_success(self, request):
        headers = self.get_headers_from_request(request, source="backend", ip_header="HTTP_X_REAL_IP")
        user_id = castle_userid(request.user) if request.user else ""
        self.make_request("events", data={"name": "$challenge.requested", "user_id": user_id}, headers=headers)

    def log_challenge_fail(self, request):
        headers = self.get_headers_from_request(request, source="backend", ip_header="HTTP_X_REAL_IP")
        user_id = castle_userid(request.user) if request.user else ""
        self.make_request("events", data={"name": "$challenge.requested", "user_id": user_id}, headers=headers)

    def get_headers_from_request(self, request, source="web", ip_header="REMOTE_ADDR"):
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
        r = requests.post(url=url, data=json.dumps(data), headers=headers, auth=('', self.api_secret), timeout=CASTLE_TIMEOUT)
        return [url, str(r.status_code), r.text, r.headers, headers, data]
