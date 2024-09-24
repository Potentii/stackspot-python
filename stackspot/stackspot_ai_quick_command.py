import json
from typing import Any

import requests
import time

from stackspot.stackspot_dict_types import QuickCommandPollExecutionOpts, StackspotAiQuickCommandExecutionCallback


class StackspotAiQuickCommand:
	def __init__(self, root):
		"""
		:param Stackspot root: The root Stackspot instance
		"""
		if not root:
			raise ValueError(f'Stackspot: Invalid root object "{root}"')
		self._root = root


	def create_execution(self, slug: str, input_data: str|dict|object|Any, conversation_id: str=None) -> str:
		"""
		Creates a new Quick Command execution. Generating a new executionId that can be queried by the 'getExecution' method.
		:param slug: The Quick Command slug identifier.
		:param input_data: The input for this execution, it can be a string, or an object/array.
		:param conversation_id: A conversation ID, this is used for continuing a previously started conversation. If it's the first call, you can ignore this field.
		:return: It returns the executionId.
		"""
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


	def get_execution(self, execution_id: str) -> StackspotAiQuickCommandExecutionCallback:
		"""
		Gets the current status of a Quick Command execution.
		:param execution_id: The Quick Command execution ID.
		:return:
		"""
		res = requests.get(
			url=f'https://genai-code-buddy-api.stackspot.com/v1/quick-commands/callback/{execution_id}',
			headers={
				'Authorization': f'Bearer {self._root.auth.get_access_token()}'
			}
		)
		if res.status_code > 299:
			raise Exception(f'{res.status_code} - QUICK_COMMAND_GET_EXECUTION_ERROR - Error getting a Quick Command execution: {res.text}')
		return res.json()


	def poll_execution(self, execution_id: str, opts:QuickCommandPollExecutionOpts | None=None) -> StackspotAiQuickCommandExecutionCallback:
		"""
		Starts polling for a Quick Command execution until its status become 'COMPLETED' or 'FAILURE'. By default it polls the callback endpoint on every 500ms, but it can be configured in the opts.
		:param execution_id: The Quick Command execution ID.
		:param opts: The options of this polling, to configure things like max attempts, timeout, delay, etc.
		:return:
		"""
		execution = None
		tries = 0
		start_ts = int(time.time())
		condition = True
		while condition is True:
			tries += 1
			execution = self.get_execution(execution_id)

			if opts and 'on_callback_response' in opts and opts['on_callback_response']:
				opts['on_callback_response'](execution)

			time.sleep((opts and 'delay' in opts and opts['delay']) or 0.5)

			condition = (('progress' not in execution or execution['progress'] is None or 'status' not in execution['progress'] or execution['progress']['status'] not in {'COMPLETED', 'FAILURE'})
							 and (opts is None or 'max_retries' not in opts or opts['max_retries'] is None or opts['max_retries'] <= 0 or tries < opts['max_retries'])
							 and (opts is None or 'max_retries_timeout' not in opts or opts['max_retries_timeout'] is None or opts['max_retries_timeout'] <= 0 or ((int(time.time()) - start_ts) < opts['max_retries_timeout'])))

		if 'progress' not in execution or execution['progress'] is None or 'status' not in execution['progress'] or execution['progress']['status'] not in {'COMPLETED', 'FAILURE'}:
			raise Exception(f'QUICK_COMMAND_EXECUTE_MAX_ATTEMPTS_REACHED_ERROR - Max attempts (by retries or time limit) reached for Quick Command execution, last execution: {json.dumps(execution) if execution is not None else None}')

		return execution