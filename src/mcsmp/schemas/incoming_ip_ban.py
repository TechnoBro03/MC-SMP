from pydantic.dataclasses import dataclass
from .player import Player
	
@dataclass
class IncomingIPBan:
	"""An incoming IP ban."""

	reason: str
	"""Reason for the ban."""

	expires: str
	"""When the ban expires, in ISO 8601 format."""

	ip: str
	"""The IP address that is banned."""

	source: str
	"""The source of the ban (e.g. "admin", "system")."""

	player: Player
	"""The player associated with the ban."""
