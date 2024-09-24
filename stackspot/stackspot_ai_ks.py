import requests

from stackspot.stackspot_dict_types import StackspotAiContentUpload


class StackspotAiKs:
	def __init__(self, root):
		"""
		:param Stackspot root: The root Stackspot instance
		"""
		if not root:
			raise ValueError(f'Stackspot: Invalid root object "{root}"')
		self._root = root


	def create_ks(self, slug: str, name: str, description: str, ks_type: str) -> None:
		"""
		Creates a new Knowledge Source.
		:param slug: The slug ID of this new KS. It must be unique, and it CANNOT be changed later.
		:param name: The KS display name.
		:param description: The KS description.
		:param ks_type: The KS type. It must be either 'API', 'SNIPPET', or 'CUSTOM'. For more information, please visit https://ai.stackspot.com/docs/knowledge-source/ks#types-of-knowledge-objects.
		:return:
		"""
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


	def batch_remove_ks_objects(self, slug: str, mode: str) -> None:
		"""
		Removes multiple objects from a Knowledge Source.
		:param slug: The slug ID of the KS.
		:param mode: The remove mode. Valid values are: 'ALL' (Removes all objects from KS), 'STANDALONE' (Removes only standalone objects), 'UPLOADED' (Removes only uploaded objects). For more information, please visit https://ai.stackspot.com/docs/knowledge-source/create-update-via-api#delete-knowledge-sources-objects.
		:return:
		"""
		if mode not in {'ALL','STANDALONE','UPLOADED'}:
			raise ValueError(f'Cannot batch remove Knowledge Source objects, invalid mode "{mode}"')

		query = {} if mode == 'ALL' else {'standalone': mode == 'STANDALONE'}

		res = requests.delete(
			url=f'https://genai-code-buddy-api.stackspot.com/v1/knowledge-sources/{slug}/objects',
			params=query,
			headers={'Authorization': f'Bearer {self._root.auth.get_access_token()}'},
		)
		if res.status_code > 299:
			raise Exception(f'{res.status_code} - KS_OBJ_BATCH_REMOVE_ERROR - Error batch removing objects from a Knowledge Source: {res.text}')


	def upload_ks_object(self, slug: str, file_name: str, content: str, upload: StackspotAiContentUpload=None) -> None:
		"""
		Uploads new content to a Knowledge Source.
		:param slug: The KS slug identifier.
		:param file_name: The desired file name.
		:param content: The content to upload, it can be a buffer or a string.
		:param upload: If you want to reuse another upload form to upload more files, you can pass it here. It must be a 'KNOWLEDGE_SOURCE' upload form, otherwise this might upload the content to an undesired location.
		:return:
		"""
		if upload is None:
			upload = self._root.ai.open_upload_content_form('KNOWLEDGE_SOURCE', slug, file_name)

		return self._root.ai.upload_content(upload, content)

