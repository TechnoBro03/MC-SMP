from dataclasses import asdict
from typing import TYPE_CHECKING, Awaitable, Callable, Final
from pyeventic import event
from mcsmp.jsonrpc.request import Request
from mcsmp.schemas import TypedGameRule, UntypedGameRule
if TYPE_CHECKING:
	from mcsmp.client import Client

class Gamerules:
	"""Gamerule endpoints."""

	method: Final[str] = "minecraft:gamerules"
	notification: Final[str] = "minecraft:notification/gamerules"

	def __init__(self, client: "Client"):
		self._client = client

		self._endpoints: dict[str, Callable[[Request], Awaitable[None]]] = {
			f"{self.notification}/updated": lambda n: self.updated(TypedGameRule(**n.params[0]))
		}
		client.on_notification.subscribe(lambda n: evt(n) if (evt := self._endpoints.get(n.method)) else None) # type: ignore

	async def get(self) -> list[TypedGameRule]:
		"""
		Get the available game rule keys and their current values.

		:return: A list of TypedGameRules representing the current game rules.
		:rtype: list[TypedGameRule]
		"""
		response = await self._client.request(self.method)
		return [TypedGameRule(**r) for r in response]
	
	async def update(self, gamerule: UntypedGameRule) -> TypedGameRule:
		"""
		Update a game rule to the provided value.

		:param gamerule: An UntypedGameRule representing the game rule to update.
		:type gamerule: UntypedGameRule
		:return: A TypedGameRule representing the updated game rule.
		:rtype: TypedGameRule
		"""
		params = {"gamerule": asdict(gamerule)}
		response = await self._client.request(f"{self.method}/update", params=params)
		return TypedGameRule(**response)
	
	@event
	async def updated(self, gamerule: TypedGameRule) -> None:
		"""
		Called when a gamerule is updated.

		:param gamerule: The updated gamerule.
		:type gamerule: TypedGameRule
		"""