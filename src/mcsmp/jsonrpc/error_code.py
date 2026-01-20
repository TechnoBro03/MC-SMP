from enum import IntEnum

class ErrorCode(IntEnum):
	"""The standard JSON-RPC 2.0 error codes."""

	PARSE_ERROR = -32700
	"""
	Invalid JSON was received by the server. An error occurred on the server while parsing the JSON text.
	"""

	INVALID_REQUEST = -32600
	"""
	The JSON sent is not a valid Request object.
	"""

	METHOD_NOT_FOUND = -32601
	"""
	The method does not exist or is not available.
	"""

	INVALID_PARAMS = -32602
	"""
	Invalid method parameter(s).
	"""

	INTERNAL_ERROR = -32603
	"""
	A server error occurred while processing the request.
	"""

	SERVER_ERROR = -32000
	"""
	Server error. Reserved for implementation-defined server-errors.
	"""