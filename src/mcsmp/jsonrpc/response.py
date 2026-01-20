from typing import Any, Generator
from pydantic.dataclasses import dataclass
from .error import Error

@dataclass
class Response:
	"""A JSON-RPC response."""

	id: str | int
	"""A unique identifier for the request. This can be a string or a number."""

	jsonrpc: str = "2.0"
	"""JSON-RPC version (should always be "2.0")."""

	result: Any = None
	"""The result of the method call. Required on success, must not be included on error."""

	error: Error | None = None
	"""An error object if there was an error invoking the method. Required on error, must not be included on success."""

	def __post_init__(self) -> None:
		if (self.result is None) == (self.error is None):
			raise ValueError("Either 'result' or 'error' must be provided, but not both")
		if self.jsonrpc != "2.0":
			raise ValueError("Invalid JSON-RPC version, must be '2.0'")
		
	def __iter__(self) -> Generator[tuple[str, Any], None, None]:
		"""
		Custom iterator to exclude None values from serialization.
		
		:return: An iterator over the request fields.
		:rtype: Generator[tuple[str, Any], None, None]
		"""
		for slot in self.__dict__:
			attr = getattr(self, slot)
			if attr is not None: yield (slot, attr)
