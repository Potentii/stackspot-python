from typing import TypedDict, Any, Callable
from typing import List



# Auth
class StackspotAuthTokenResponse(TypedDict('StackspotAuthTokenResponse', { 'not-before-policy': int, })):
	access_token: str
	expires_in: int
	refresh_token: str
	refresh_expires_in: int
	token_type: str
	scope: str
	session_state: str




# AI:
class StackspotAiContentUploadForm(TypedDict('StackspotAiContentUploadForm', { 'x-amz-algorithm': str, 'x-amz-credential': str, 'x-amz-date': str, 'x-amz-security-token': str, 'x-amz-signature': str, })):
	key: str
	policy: str


class StackspotAiContentUpload(TypedDict):
	id: str
	url: str
	form: StackspotAiContentUploadForm




# AI - Quick commands:
class StackspotAiQuickCommandExecutionCallbackProgress(TypedDict):

	start: str
	"""
	* Execution start timestamp (formatted as ISO8601, example: '2024-02-15T20:48:43.990Z').
	"""
	end: str | None
	"""
	* Execution end timestamp (formatted as ISO8601, example: '2024-02-15T20:48:43.990Z').
	"""
	duration: int | None
	"""
	* Duration of the execution (in seconds).
	"""
	execution_percentage: float
	"""
	* Percentage of the execution (in a '0.00' to '1.00' range).
	"""
	status: str
	"""
	* Execution status, it can be either 'CREATED', 'RUNNING', 'FAILURE', or 'COMPLETED'.
	"""


class StackspotAiQuickCommandExecutionCallbackStepResult(TypedDict):
	status_code: int | None
	headers: dict | object | None
	data: str | None
	json_data: object | None
	answer: str | None
	sources: List[Any] | None


class StackspotAiQuickCommandExecutionCallbackStep(TypedDict):
	step_name: str
	execution_order: int
	type: str
	step_result: StackspotAiQuickCommandExecutionCallbackStepResult


class StackspotAiQuickCommandExecutionCallback(TypedDict):
	execution_id: str
	quick_command_slug: str
	conversation_id: str
	result: str | None
	progress: StackspotAiQuickCommandExecutionCallbackProgress | None
	steps: List[StackspotAiQuickCommandExecutionCallbackStep] | None


class QuickCommandPollExecutionOpts(TypedDict):
	max_retries: int | None
	"""
	The max number of polling retries. 0 (or unset) will make it try indefinitely.
	"""
	max_retries_timeout: float | None
	"""
	The max timeout (in milliseconds) of polling retries. 0 (or unset) will make it try indefinitely.
	"""
	delay: float | None
	"""
	Sets the delay between each poll request, in milliseconds. It defaults to 500ms.
	"""
	on_callback_response: Callable[[StackspotAiQuickCommandExecutionCallback], Any] | None

