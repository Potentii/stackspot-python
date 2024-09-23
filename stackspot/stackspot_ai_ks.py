import requests

class StackspotAiKs:
	def __init__(self, root):
		"""
		:param Stackspot root: The root Stackspot instance
		"""
		self._root = root


	def create_ks(self, slug, name, description, ks_type):
		res = requests.post(
			url='https://genai-code-buddy-api.stackspot.com/v1/knowledge-sources',
			json={
				'slug': slug,
				'name': name,
				'description': description,
				'type': ks_type,
			},
			headers={'Authorization': f'Bearer {self._root.auth.get_access_token()}'},
		)
		if res.status_code > 299:
			raise Exception(f'{res.status_code} - KS_CREATE_ERROR - Error creating new Knowledge Source: {res.text}')


	def batch_remove_ks_objects(self, slug, mode):
		if mode not in {'ALL','STANDALONE','UPLOADED'}:
			raise Exception(f'Cannot batch remove Knowledge Source objects, invalid mode "{mode}"')

		query = {} if mode == 'ALL' else {'standalone': mode == 'STANDALONE'}

		res = requests.delete(
			url=f'https://genai-code-buddy-api.stackspot.com/v1/knowledge-sources/{slug}/objects',
			params=query,
			headers={'Authorization': f'Bearer {self._root.auth.get_access_token()}'},
		)
		if res.status_code > 299:
			raise Exception(f'{res.status_code} - KS_OBJ_BATCH_REMOVE_ERROR - Error batch removing objects from a Knowledge Source: {res.text}')


	def upload_ks_object(self, slug, file_name, content, upload=None):
		if upload is None:
			upload = self._root.ai.open_upload_content_form('KNOWLEDGE_SOURCE', slug, file_name)

		return self._root.ai.upload_content(upload, content)

