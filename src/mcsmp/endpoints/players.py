from dataclasses import asdict
from typing import TYPE_CHECKING, Awaitable, Callable, Final
from pyeventic import event
from mcsmp.jsonrpc.request import Request
from mcsmp.schemas import Player, KickPlayer
if TYPE_CHECKING:
	from mcsmp.client import Client

class Players:
	"""Player endpoints"""

	method: Final[str] = "minecraft:players"
	notification: Final[str] = "minecraft:notification/players"

	def __init__(self, client: "Client"):
		self._client = client

		self._endpoints: dict[str, Callable[[Request], Awaitable[None]]] = {
			f"{self.notification}/joined": lambda n: self.joined(Player(**n.params[0])),
			f"{self.notification}/left": lambda n: self.left(Player(**n.params[0])),
		}
		client.on_notification.subscribe(lambda n: evt(n) if (evt := self._endpoints.get(n.method)) else None) # type: ignore

	async def get(self) -> list[Player]:
		"""
		Get all connected players.

		:return: A list of Players representing the current connected players.
		:rtype: list[Player]
		"""
		response = await self._client.request(self.method)
		return [Player(**p) for p in response]
	
	async def kick(self, kick: list[KickPlayer]) -> list[Player]:
		"""
		Kick players from the server.

		:param kick: A list of KickPlayers representing the players to kick.
		:type kick: list[KickPlayer]
		:return: A list of Players representing the kicked players.
		:rtype: list[Player]
		"""
		params = {"kick": [asdict(k) for k in kick]}
		response = await self._client.request(f"{self.method}/kick", params=params)
		return [Player(**p) for p in response]
	
	@event
	async def joined(self, player: Player) -> None:
		"""
		Called when a player joins.

		:param player: The player who joined.
		:type player: Player
		"""

	@event
	async def left(self, player: Player) -> None:
		"""
		Called when a player leaves.

		:param player: The player who left.
		:type player: Player
		"""