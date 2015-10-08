import json
from django.conf import settings

__author__ = 'jens'
import requests

CASTLEIO_TIMEOUT = getattr(settings, "CASTLEIO_TIMEOUT", 10)

class CastleIO(object):
	api_secret = ""
	api_url = ""

	def __init__(self, api_secret=None, api_url=None):
		if not api_url:
			api_url = getattr(settings, "CASTLEIO_API_URL", "https://api.castle.io/v1/")
			self.api_url = api_url
		if not api_secret:
			api_secret = getattr(settings, "CASTLEIO_API_SECRET")
			self.api_secret = api_secret

	def log_login_success(self, user, request):
		headers = self.get_headers_from_request(request)
		self.make_request("events",data={"name": "$login.succeeded", "user_id": str(user.id)}, headers=headers)

	def log_logout_success(self, user, request):
		headers = self.get_headers_from_request(request)
		self.make_request("events",data={"name": "$logout.succeeded", "user_id": str(user.id)}, headers=headers)

	def get_headers_from_request(self, request):
		return {
			"X-Castle-Cookie-Id" : request.COOKIES.get("__cid"),
			"X-Castle-Ip" : request.META.get("REMOTE_ADDR"),
			"X-Castle-Headers" : json.dumps({
				"User-Agent" : request.META.get("USER_AGENT"),
				"Accept": request.META.get("HTTP_ACCEPT"),
				"Accept-Encoding" : request.META.get("HTTP_ACCEPT_ENCODING"),
				"Accept-Language" : request.META.get("HTTP_ACCEPT_LANGUAGE"),
			})
		}

	def make_request(self, endpoint, data, headers):
		url = "%s/%s" % (self.api_url, endpoint)
		requests.post(url=url, data=data, headers=headers, auth=('', self.api_secret), timeout=CASTLEIO_TIMEOUT)