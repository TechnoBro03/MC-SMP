from dataclasses import asdict
from typing import Awaitable, Callable, TYPE_CHECKING, Final
from pyeventic import event
from mcsmp.schemas import Player, UserBan
from mcsmp.jsonrpc import Request
if TYPE_CHECKING:
	from mcsmp import Client

class Bans:
	"""Ban endpoints."""

	method: Final[str] = "minecraft:bans"
	notification: Final[str] = "minecraft:notification/bans"

	def __init__(self, client: "Client"):
		self._client = client

		self._endpoints: dict[str, Callable[[Request], Awaitable[None]]] = {
			f"{self.notification}/added": lambda n: self.added(UserBan(**n.params[0])),
			f"{self.notification}/removed": lambda n: self.removed(Player(**n.params[0])),
		}
		client.on_notification.subscribe(lambda n: evt(n) if (evt := self._endpoints.get(n.method)) else None) # type: ignore

	async def get(self) -> list[UserBan]:
		"""
		Get the ban list.

		:return: A list of UserBans representing the current ban list.
		:rtype: list[UserBan]
		"""
		response = await self._client.request(self.method)
		return [UserBan(**u) for u in response]
	
	async def set(self, bans: list[UserBan]) -> list[UserBan]:
		"""
		Set the ban list to the provided list of UserBans.

		:param bans: A list of UserBans to set as the ban list.
		:type bans: list[UserBan]
		:return: A list of UserBans representing the updated ban list.
		:rtype: list[UserBan]
		"""
		params = {"bans": [asdict(b) for b in bans]}
		response = await self._client.request(f"{self.method}/set", params=params)
		return [UserBan(**u) for u in response]
	
	async def add(self, bans: list[UserBan]) -> list[UserBan]:
		"""
		Add players to the ban list.

		:param bans: A list of UserBans to add to the ban list.
		:type bans: list[UserBan]
		:return: A list of UserBans representing the updated ban list.
		:rtype: list[UserBan]
		"""
		params = {"add": [asdict(b) for b in bans]}
		response = await self._client.request(f"{self.method}/add", params=params)
		return [UserBan(**u) for u in response]
	
	async def remove(self, bans: list[Player]) -> list[UserBan]:
		"""
		Remove players from the ban list.

		:param bans: A list of Players to remove from the ban list.
		:type bans: list[Player]
		:return: A list of UserBans representing the updated ban list.
		:rtype: list[UserBan]
		"""
		params = {"remove": [asdict(b) for b in bans]}
		response = await self._client.request(f"{self.method}/remove", params=params)
		return [UserBan(**u) for u in response]
	
	async def clear(self) -> list[UserBan]:
		"""
		Clear all players in the ban list.

		:return: A list of UserBans representing the updated (empty) ban list.
		:rtype: list[UserBan]
		"""
		response = await self._client.request(f"{self.method}/clear")
		return [UserBan(**u) for u in response]
	
	@event
	async def added(self, player: UserBan) -> None:
		"""
		Called when a player is added to the ban list.
		
		:param player: The player who was added to the ban list.
		:type player: UserBan
		"""

	@event
	async def removed(self, player: Player) -> None:
		"""
		Called when a player is removed from the ban list.
		
		:param player: The player who was removed from the ban list.
		:type player: Player
		"""