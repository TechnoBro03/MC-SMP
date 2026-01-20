import uuid
from pydantic.dataclasses import dataclass

@dataclass
class Player:
	"""A player."""

	name: str | None = None
	"""The name of the player."""

	id: str | None = None
	"""The UUID of the player."""

	def __post_init__(self) -> None:
		if self.id is None and self.name is None:
			raise ValueError("Either player 'name' or 'id' must be provided.")
		try: uuid.UUID(self.id) if self.id else None
		except ValueError: raise ValueError(f"Invalid UUID format for player ID: {self.id}")