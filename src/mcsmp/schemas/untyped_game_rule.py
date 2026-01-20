from pydantic.dataclasses import dataclass

@dataclass
class UntypedGameRule:
	"""A gamerule with an unknown type."""

	key: str
	"""The key of the game rule."""

	value: str | bool
	"""The value of the game rule as a string or boolean."""