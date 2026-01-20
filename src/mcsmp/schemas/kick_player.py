from pydantic.dataclasses import dataclass
from .message import Message
from .player import Player

@dataclass
class KickPlayer:
	"""A kick action."""

	player: Player
	"""The player being kicked."""

	reason: Message
	"""The reason for the kick."""