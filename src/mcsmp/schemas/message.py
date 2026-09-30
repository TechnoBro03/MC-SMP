from pydantic.dataclasses import dataclass

@dataclass
class Message:
	"""A message."""

	translatable: str | None = None
	"""The translatable key."""

	translatableParams: list[str] | None = None
	"""The parameters for the translatable key."""

	literal: str | None = None
	"""The literal message."""

	def __post_init__(self) -> None:
		if self.translatable is None and self.literal is None:
			raise ValueError("Either message 'translatable' or 'literal' must be provided.")
