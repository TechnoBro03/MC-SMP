from pydantic.dataclasses import dataclass
from .player import Player
from .version import Version

@dataclass
class ServerState:
	"""The server state."""

	players: list[Player]
	"""The list of players currently on the server."""

	started: bool
	"""Whether the server has started."""

	version: Version
	"""The server version."""