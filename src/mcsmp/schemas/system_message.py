from pydantic.dataclasses import dataclass
from .player import Player
from .message import Message

@dataclass
class SystemMessage:
	"""A system message."""

	receivingPlayers: list[Player]
	"""The players receiving the system message."""

	overlay: bool
	"""Whether the message is an overlay."""

	message: Message
	"""The message content."""