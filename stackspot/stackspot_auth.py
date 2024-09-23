import time

import requests

class StackspotAuth:
	def __init__(self, root):
		"""
		:param Stackspot root: The root Stackspot instance
		"""
		self._root = root
		self._token_response = None
		self._get_at = None


	def _fetch_token(self):
		res = requests.post(
			url=f'https://idm.stackspot.com/{self._root._realm}/oidc/oauth/token',
			data={
				'grant_type': 'client_credentials',
				'client_id': self._root._client_id,
				'client_secret': self._root._client_secret
			}
		)
		if res.status_code > 299:
			raise Exception(f'{res.status_code} - AUTH_ERROR - Error while authenticating on Stackspot: {res.text}')
		return res.json()


	def get_access_token(self):
		if self._token_response is None or self._token_response['access_token'] is None or ((self._get_at + self._token_response['expires_in']) <= time.time()):
			self._token_response = self._fetch_token()
			self._get_at = time.time()
		return self._token_response['access_token']


	def _invalidate_token(self):
		self._token_response = None