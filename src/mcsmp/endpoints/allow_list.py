from dataclasses import asdict
from typing import Awaitable, Callable, TYPE_CHECKING, Final
from pyeventic import event
from mcsmp.jsonrpc import Request
from mcsmp.schemas import Player
if TYPE_CHECKING:
	from mcsmp import Client

class AllowList:
	"""Allow list endpoints."""

	method: Final[str] = "minecraft:allowlist"
	notification: Final[str] = "minecraft:notification/allowlist"

	def __init__(self, client: "Client") -> None:
		self._client = client

		self._endpoints: dict[str, Callable[[Request], Awaitable[None]]] = {
			f"{self.notification}/added": lambda n: self.added(Player(**n.params[0])),
			f"{self.notification}/removed": lambda n: self.removed(Player(**n.params[0])),
		}
		client.on_notification.subscribe(lambda n: evt(n) if (evt := self._endpoints.get(n.method)) else None) # type: ignore

	async def get(self) -> list[Player]:
		"""
		Get the allow list.

		:return: A list of Players representing the current allow list.
		:rtype: list[Player]
		"""
		response = await self._client.request(self.method)
		return [Player(**p) for p in response]

	async def set(self, players: list[Player]) -> list[Player]:
		"""
		Set the allow list to the provided list of players.

		:param players: A list of Players to set as the allow list.
		:type players: list[Player]
		:return: A list of Players representing the updated allow list.
		:rtype: list[Player]
		"""
		params = {"players": [asdict(p) for p in players]}
		response = await self._client.request(f"{self.method}/set", params=params)
		return [Player(**p) for p in response]

	async def add(self, players: list[Player]) -> list[Player]:
		"""
		Add players to the allow list.

		:param players: A list of Players to add to the allow list.
		:type players: list[Player]
		:return: A list of Players representing the updated allow list.
		:rtype: list[Player]
		"""
		params = {"add": [asdict(p) for p in players]}
		response = await self._client.request(f"{self.method}/add", params=params)
		return [Player(**p) for p in response]

	async def remove(self, players: list[Player]) -> list[Player]:
		"""
		Remove players from the allow list.
		
		:param players: A list of Players to remove from the allow list.
		:type players: list[Player]
		:return: A list of Players representing the updated allow list.
		:rtype: list[Player]
		"""
		params = {"remove": [asdict(p) for p in players]}
		response = await self._client.request(f"{self.method}/remove", params=params)
		return [Player(**p) for p in response]

	async def clear(self) -> list[Player]:
		"""
		Clear all players in the allow list.

		:return: A list of Players representing the updated (empty) allow list.
		:rtype: list[Player]
		"""
		response = await self._client.request(f"{self.method}/clear")
		return [Player(**p) for p in response]
	
	@event
	async def added(self, player: Player) -> None:
		"""
		Called when a player is added to the allowlist.
		
		:param player: The player who was added to the allowlist.
		:type player: Player
		"""

	@event
	async def removed(self, player: Player) -> None:
		"""
		Called when a player is removed from the allowlist.
		
		:param player: The player who was removed from the allowlist.
		:type player: Player
		"""