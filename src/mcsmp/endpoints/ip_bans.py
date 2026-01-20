from dataclasses import asdict
from typing import TYPE_CHECKING, Awaitable, Callable, Final
from pyeventic import event
from mcsmp.jsonrpc.request import Request
from mcsmp.schemas import IPBan, IncomingIPBan
if TYPE_CHECKING:
	from mcsmp.client import Client

class IPBans:
	"""IP ban endpoints."""

	method: Final[str] = "minecraft:ip_bans"
	notification: Final[str] = "minecraft:notification/ip_bans"

	def __init__(self, client: "Client"):
		self._client = client

		self._endpoints: dict[str, Callable[[Request], Awaitable[None]]] = {
			f"{self.notification}/added": lambda n: self.added(IPBan(**n.params[0])),
			f"{self.notification}/removed": lambda n: self.removed(n.params[0]),
		}
		client.on_notification.subscribe(lambda n: evt(n) if (evt := self._endpoints.get(n.method)) else None) # type: ignore

	async def get(self) -> list[IPBan]:
		"""
		Get the IP ban list.

		:return: A list of IPBans representing the current IP ban list.
		:rtype: list[IPBan]
		"""
		response = await self._client.request(self.method)
		return [IPBan(**b) for b in response]
	
	async def set(self, bans: list[IPBan]) -> list[IPBan]:
		"""
		Set the IP ban list to the provided list of IPBans.
		
		:param bans: A list of IPBans to set as the IP ban list.
		:type bans: list[IPBan]
		:return: A list of IPBans representing the updated IP ban list.
		:rtype: list[IPBan]
		"""
		params = {"banlist": [asdict(b) for b in bans]}
		response = await self._client.request(f"{self.method}/set", params=params)
		return [IPBan(**b) for b in response]

	async def add(self, bans: list[IncomingIPBan]) -> list[IPBan]:
		"""
		Add IPs to the IP ban list.

		:param bans: A list of IncomingIPBans to add to the IP ban list.
		:type bans: list[IncomingIPBan]
		:return: A list of IPBans representing the updated IP ban list.
		:rtype: list[IPBan]
		"""
		params = {"add": [asdict(b) for b in bans]}
		response = await self._client.request(f"{self.method}/add", params=params)
		return [IPBan(**b) for b in response]

	async def remove(self, bans: list[str]) -> list[IPBan]:
		"""
		Remove IPs from the IP ban list.

		:param bans: A list of IP addresses (as strings) to remove from the IP ban list.
		:type bans: list[str]
		:return: A list of IPBans representing the updated IP ban list.
		:rtype: list[IPBan]
		"""
		params = {"ip": bans}
		response = await self._client.request(f"{self.method}/remove", params=params)
		return [IPBan(**b) for b in response]

	async def clear(self) -> list[IPBan]:
		"""
		Clear all IPs in the IP ban list.
		
		:return: A list of IPBans representing the updated IP ban list.
		:rtype: list[IPBan]
		"""
		response = await self._client.request(f"{self.method}/clear")
		return [IPBan(**b) for b in response]
	
	@event
	async def added(self, player: IPBan) -> None:
		"""
		Called when an IP is added to the ip ban list.

		:param player: The IP that was added to the ip ban list.
		:type player: IPBan
		"""

	@event
	async def removed(self, player: str) -> None:
		"""
		Called when an IP is removed from the ip ban list.

		:param player: The IP that was removed from the ip ban list.
		:type player: str
		"""