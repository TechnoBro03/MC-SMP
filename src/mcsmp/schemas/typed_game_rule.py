from typing import Literal
from pydantic.dataclasses import dataclass

@dataclass
class TypedGameRule:
	"""A gamerule with a specific type."""

	type: Literal["boolean", "integer"]
	"""The type of the gamerule."""

	key: str
	"""The key of the gamerule."""

	value: bool | int
	"""The value of the gamerule."""