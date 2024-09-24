import requests

from .stackspot_ai_ks import StackspotAiKs
from .stackspot_ai_quick_command import StackspotAiQuickCommand
from .stackspot_dict_types import StackspotAiContentUpload


class StackspotAi:
	def __init__(self, root):
		"""
		:param Stackspot root: The root Stackspot instance
		"""
		if not root:
			raise ValueError(f'Stackspot: Invalid root object "{root}"')
		self._root = root
		self.ks = StackspotAiKs(self._root)
		self.quick_command = StackspotAiQuickCommand(self._root)


	def open_upload_content_form(self, target_type: str, target_id: str, file_name: str, expiration: int = 600) -> StackspotAiContentUpload:
		"""
		Starts a new upload form, call this method before attempting to upload any file, and use the returned information to execute the upload itself. But be aware that some upload methods already opens a new form by default.
		:param target_type: The target type to upload this file (e.g. 'KNOWLEDGE_SOURCE').
		:param target_id: The target ID (if it's a KS, use the KS slug identifier).
		:param file_name: The desired name of the file.
		:param expiration: The form's expiration timeout (in seconds), defaults to 600.
		:return:
		"""
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


	def upload_content(self, upload: StackspotAiContentUpload, content: str) -> None:
		"""
		Uploads a new content to an open Upload form.
		:param upload: The upload form, use the {@code openUploadContentForm} to open a new one.
		:param content: The content to upload, it can be a buffer or a string.
		:return:
		"""
		form = upload['form'].copy()
		form['file'] = content

		res = requests.post(
			url=upload['url'],
			files=dict(form),
		)
		if res.status_code > 299:
			raise Exception(f'{res.status_code} - UPLOAD_ERROR - Error uploading new content: {res.text}')