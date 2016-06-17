import json
from django.conf import settings
from templatetags.castle import castle_userid
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
        headers = self.get_headers_from_request(request)
        user_id = castle_userid(user) if user else ""
        self.make_request("events", data={"name": "$login.succeeded", "user_id": user_id}, headers=headers)

    def log_logout_success(self, user, request):
        headers = self.get_headers_from_request(request)
        user_id = castle_userid(user) if user else ""
        self.make_request("events", data={"name": "$logout.succeeded", "user_id": user_id}, headers=headers)

    def log_login_fail(self, credentials):
        username = credentials.get("username", None)
        password = credentials.get("password", None)
        request = credentials.get("request", None)
        headers = self.get_headers_from_request(request)
        return self.make_request("events", data={"name": "$login.failed", "details": {"$login": "username"}}, headers=headers)

    def get_headers_from_request(self, request):
        return {
            "X-Castle-Cookie-Id": request.COOKIES.get("__cid"),
            "X-Castle-Ip": request.META.get('HTTP_X_REAL_IP', request.META.get('REMOTE_ADDR', '127.0.0.1')),
            "X-Castle-Headers": json.dumps({
                "User-Agent": request.META.get("HTTP_USER_AGENT"),
                "Accept": request.META.get("HTTP_ACCEPT"),
                "Accept-Encoding": request.META.get("HTTP_ACCEPT_ENCODING"),
                "Accept-Language": request.META.get("HTTP_ACCEPT_LANGUAGE"),
            }),
            "X-Castle-Source": "backend"
        } if request else {}

    def make_request(self, endpoint, data, headers):
        url = "%s/%s" % (self.api_url, endpoint)
        r = requests.post(url=url, data=json.dumps(data), headers=headers, auth=('', self.api_secret), timeout=CASTLE_TIMEOUT)
        return [url, str(r.status_code), r.text, r.headers, headers, data]
