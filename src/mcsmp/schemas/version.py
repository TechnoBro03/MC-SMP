from pydantic.dataclasses import dataclass

@dataclass
class Version:
	"""A version."""

	protocol: int
	"""The version protocol."""

	name: str
	"""The version name."""