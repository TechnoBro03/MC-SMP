from pydantic.dataclasses import dataclass
from .player import Player

@dataclass
class Operator:
	"""An operator."""

	permissionLevel: int
	"""The permission level of the operator."""

	bypassPlayerLimit: bool
	"""Whether the operator can bypass the player limit."""

	player: Player
	"""The operator player."""