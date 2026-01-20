from typing import Any, Generator
from pydantic.dataclasses import dataclass

@dataclass
class Request:
	"""A JSON-RPC request. Used for both requests and notifications."""

	method: str
	"""The method name to call (e.g., "rpc.discover", "minecraft:allowlist/add")."""

	jsonrpc: str = "2.0"
	"""JSON-RPC version (should always be "2.0")."""

	id: str | int | None = None
	"""A unique identifier for the request. This can be a string or a number. Absent for notifications."""

	params: Any = None
	"""The parameters to send with the request (eg., {"key1": "value1"}, ["value1", "value2"])."""

	def __post_init__(self) -> None:
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