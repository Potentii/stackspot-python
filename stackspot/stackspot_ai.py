import requests

from .stackspot_ai_ks import StackspotAiKs
from .stackspot_ai_quick_command import StackspotAiQuickCommand


class StackspotAi:
	def __init__(self, root):
		"""
		:param Stackspot root: The root Stackspot instance
		"""
		self._root = root
		self.ks = StackspotAiKs(self._root)
		self.quick_command = StackspotAiQuickCommand(self._root)


	def open_upload_content_form(self, target_type, target_id, file_name, expiration = 600):
		res = requests.post(
			url='https://genai-code-buddy-api.stackspot.com/v1/file-upload/form',
			json={
				'target_type': target_type,
				'target_id': target_id,
				'file_name': file_name,
				'expiration': expiration,
			},
			headers={'Authorization': f'Bearer {self._root.auth.get_access_token()}'},
		)
		if res.status_code > 299:
			raise Exception(f'{res.status_code} - UPLOAD_FORM_CREATE_ERROR - Error opening new upload form: {res.text}')
		return res.json()


	def upload_content(self, upload, content):
		form = upload['form'].copy()
		form['file'] = content

		res = requests.post(
			url=upload['url'],
			files=dict(form),
		)
		if res.status_code > 299:
			raise Exception(f'{res.status_code} - UPLOAD_ERROR - Error uploading new content: {res.text}')