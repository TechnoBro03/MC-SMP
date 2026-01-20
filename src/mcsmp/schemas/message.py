from pydantic.dataclasses import dataclass

@dataclass
class Message:
	"""A message."""

	translatable: str
	"""The translatable key."""

	translatableParams: list[str]
	"""The parameters for the translatable key."""

	literal: str
	"""The literal message."""