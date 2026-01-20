from pydantic.dataclasses import dataclass
from .player import Player

@dataclass
class UserBan:
	"""A user ban."""

	reason: str
	"""The reason for the ban."""

	expires: str
	"""The expiration date of the ban in ISO 8601 format."""

	source: str
	"""The source of the ban (e.g., admin, system)."""

	player: Player
	"""The banned player."""