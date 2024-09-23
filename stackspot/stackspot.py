import os
from .stackspot_ai import StackspotAi
from .stackspot_auth import StackspotAuth


class Stackspot:
	_instance = None


	def __init__(self, opts=None):
		self._client_id = None
		self._client_secret = None
		self._realm = None
		self.auth = StackspotAuth(self)
		self.ai = StackspotAi(self)
		self.config(opts)


	@staticmethod
	def instance():
		if Stackspot._instance is None:
			Stackspot._instance = Stackspot()
		return Stackspot._instance


	def config(self, opts=None):
		self._client_id = (opts and opts.client_id) or os.environ.get('STACKSPOT_CLIENT_ID')
		self._client_secret = (opts and opts.client_secret) or os.environ.get('STACKSPOT_CLIENT_SECRET')
		self._realm = (opts and opts.realm) or os.environ.get('STACKSPOT_REALM')
		self.auth._invalidate_token()


	def set_client_id(self, client_id):
		self._client_id = client_id
		self.auth._invalidate_token()
		return self


	def set_client_secret(self, client_secret):
		self._client_secret = client_secret
		self.auth._invalidate_token()
		return self


	def set_realm(self, realm):
		self._realm = realm
		self.auth._invalidate_token()
		return self

