import json
import requests
import time

class StackspotAiQuickCommand:
	def __init__(self, root):
		"""
		:param Stackspot root: The root Stackspot instance
		"""
		self._root = root


	def create_execution(self, slug, input_data, conversation_id=None):
		body = {'input_data': input_data} \
			if type(input_data) is str \
			else {'json': json.dumps(input_data)}

		res = requests.post(
			url=f'https://genai-code-buddy-api.stackspot.com/v1/quick-commands/create-execution/{slug}',
			params={'conversationId': conversation_id},
			json=body,
			headers={
				'Content-Type': 'application/json',
				'Authorization': f'Bearer {self._root.auth.get_access_token()}'
			}
		)
		if res.status_code > 299:
			raise Exception(f'{res.status_code} - QUICK_COMMAND_CREATE_EXECUTION_ERROR - Error creating new Quick Command execution: {res.text}')
		return res.text.replace('"', '')


	def get_execution(self, execution_id):
		res = requests.get(
			url=f'https://genai-code-buddy-api.stackspot.com/v1/quick-commands/callback/{execution_id}',
			headers={
				'Authorization': f'Bearer {self._root.auth.get_access_token()}'
			}
		)
		if res.status_code > 299:
			raise Exception(f'{res.status_code} - QUICK_COMMAND_GET_EXECUTION_ERROR - Error getting a Quick Command execution: {res.text}')
		return res.json()


	def poll_execution(self, execution_id, opts=None):
		execution = None
		tries = 0
		start_ts = int(time.time())
		condition = True
		while condition is True:
			tries += 1
			execution = self.get_execution(execution_id)
			time.sleep(0.5)

			condition = ((execution['progress'] is None or execution['progress']['status'] not in {'COMPLETED', 'FAILURE'})
							 and (opts is None or opts.max_retries is None or opts.max_retries <= 0 or tries < opts.max_retries)
							 and (opts is None or opts.max_retires_timeout is None or opts.max_retires_timeout <= 0 or ((int(time.time()) - start_ts) < opts.max_retires_timeout)))

		if execution['progress'] is None or execution['progress']['status'] not in {'COMPLETED', 'FAILURE'}:
			raise Exception(f'QUICK_COMMAND_EXECUTE_MAX_ATTEMPTS_REACHED_ERROR - Max attempts (by retries or time limit) reached for Quick Command execution, last execution: {json.dumps(execution) if execution is not None else None}')

		return execution