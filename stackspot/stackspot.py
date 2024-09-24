import os
from .stackspot_ai import StackspotAi
from .stackspot_auth import StackspotAuth


class Stackspot:
	_instance = None


	def __init__(self, opts=None):
		"""
		Creates a new Stackspot instance.
		:param opts: The Stackspot options, if not set it will use the environment variables to configure this instance.
		"""
		self._client_id = None
		self._client_secret = None
		self._realm = None
		self.auth = StackspotAuth(self)
		self.ai = StackspotAi(self)
		self.config(opts)


	@staticmethod
	def instance():
		"""
		Gets the global Stackspot singleton instance.
		:return:
		"""
		if Stackspot._instance is None:
			Stackspot._instance = Stackspot()
		return Stackspot._instance


	def config(self, opts=None):
		"""
		Completely reconfigure this Stackspot instance.
		:param opts: The new Stackspot options, if not set it will use the environment variables to configure this instance.
		:return:
		"""
		self._client_id = (opts and 'client_id' in opts and opts['client_id']) or os.environ.get('STACKSPOT_CLIENT_ID')
		self._client_secret = (opts and 'client_secret' in opts and opts['client_secret']) or os.environ.get('STACKSPOT_CLIENT_SECRET')
		self._realm = (opts and 'realm' in opts and opts['realm']) or os.environ.get('STACKSPOT_REALM')
		self.auth._invalidate_token()


	def set_client_id(self, client_id):
		"""
		Sets the clientId.
		:param client_id:
		:return:
		"""
		self._client_id = client_id
		self.auth._invalidate_token()
		return self


	def set_client_secret(self, client_secret):
		"""
		Sets the clientSecret.
		:param client_secret:
		:return:
		"""
		self._client_secret = client_secret
		self.auth._invalidate_token()
		return self


	def set_realm(self, realm):
		"""
		Sets the realm.
		:param realm:
		:return:
		"""
		self._realm = realm
		self.auth._invalidate_token()
		return self

