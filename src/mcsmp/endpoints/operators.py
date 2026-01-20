from dataclasses import asdict
from typing import TYPE_CHECKING, Awaitable, Callable, Final
from pyeventic import event
from mcsmp.jsonrpc.request import Request
from mcsmp.schemas import Operator, Player
if TYPE_CHECKING:
	from mcsmp.client import Client

class Operators:
	"""Operator endpoints."""

	method: Final[str] = "minecraft:operators"
	notification: Final[str] = "minecraft:notification/operators"

	def __init__(self, client: "Client"):
		self._client = client

		self._endpoints: dict[str, Callable[[Request], Awaitable[None]]] = {
			f"{self.notification}/added": lambda n: self.added(Operator(**n.params[0])),
			f"{self.notification}/removed": lambda n: self.removed(Operator(**n.params[0])),
		}
		client.on_notification.subscribe(lambda n: evt(n) if (evt := self._endpoints.get(n.method)) else None) # type: ignore

	async def get(self) -> list[Operator]:
		"""
		Get all oped players.

		:return: A list of Operators representing the current oped players.
		:rtype: list[Operator]
		"""
		response = await self._client.request(self.method)
		return [Operator(**o) for o in response]
	
	async def set(self, operators: list[Operator]) -> list[Operator]:
		"""
		Set the oped players to the provided list of Operators.

		:param operators: A list of Operators to set as the oped players.
		:type operators: list[Operator]
		:return: A list of Operators representing the updated oped players.
		:rtype: list[Operator]
		"""
		params = {"operators": [asdict(o) for o in operators]}
		response = await self._client.request(f"{self.method}/set", params=params)
		return [Operator(**o) for o in response]
	
	async def add(self, operators: list[Operator]) -> list[Operator]:
		"""
		Add players to the oped players.
		
		:param operators: A list of Operators to add to the oped players.
		:type operators: list[Operator]
		:return: A list of Operators representing the updated oped players.
		:rtype: list[Operator]
		"""
		params = {"add": [asdict(o) for o in operators]}
		response = await self._client.request(f"{self.method}/add", params=params)
		return [Operator(**o) for o in response]
	
	async def remove(self, operators: list[Player]) -> list[Operator]:
		"""
		Remove players from the oped players.

		:param operators: A list of Players to remove from the oped players.
		:type operators: list[Player]
		:return: A list of Operators representing the updated oped players.
		:rtype: list[Operator]
		"""
		params = {"remove": [asdict(o) for o in operators]}
		response = await self._client.request(f"{self.method}/remove", params=params)
		return [Operator(**o) for o in response]
	
	async def clear(self) -> list[Operator]:
		"""
		Clear all oped players.

		:return: A list of Operators representing the updated (empty) oped players.
		:rtype: list[Operator]
		"""
		response = await self._client.request(f"{self.method}/clear")
		return [Operator(**o) for o in response]
	

	@event
	async def added(self, player: Operator) -> None:
		"""
		Called when a player is opped.

		:param player: The player who was opped.
		:type player: Operator
		"""

	@event
	async def removed(self, player: Operator) -> None:
		"""
		Called when a player is deopped.

		:param player: The player who was deopped.
		:type player: Operator
		"""