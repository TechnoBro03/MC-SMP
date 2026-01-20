from typing import Any
from pydantic.dataclasses import dataclass

@dataclass
class Error:
	"""A JSON-RPC error."""

	code: int
	"""The error code."""

	message: str
	"""A short description of the error. The message should be limited to a concise single sentence."""

	data: Any = None
	"""
	A primitive or structured value that contains additional information about the error.
	The value of this member is defined by the server (e.g., detailed error information, nested errors etc.).
	If omitted, data has the value of None, representing that nothing was provided.
	"""