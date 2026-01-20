from dataclasses import asdict
from typing import TYPE_CHECKING, Awaitable, Callable, Final
from pyeventic import event
from mcsmp.jsonrpc.request import Request
from mcsmp.schemas import ServerState, SystemMessage
if TYPE_CHECKING:
	from mcsmp.client import Client

class Server:
	"""Server endpoints."""

	method: Final[str] = "minecraft:server"
	notification: Final[str] = "minecraft:notification/server"

	def __init__(self, client: "Client"):
		self._client = client

		self._endpoints: dict[str, Callable[[Request], Awaitable[None]]] = {
			f"{self.notification}/started": lambda n: self.started(),
			f"{self.notification}/stopping": lambda n: self.stopping(),
			f"{self.notification}/saving": lambda n: self.saving(),
			f"{self.notification}/saved": lambda n: self.saved(),
			f"{self.notification}/status": lambda n: self.heartbeat(ServerState(**n.params[0])),
			f"{self.notification}/activity": lambda n: self.activity(),
		}
		client.on_notification.subscribe(lambda n: evt(n) if (evt := self._endpoints.get(n.method)) else None) # type: ignore

	async def status(self) -> ServerState:
		"""
		Get the server status.

		:return: A ServerState representing the current server status.
		:rtype: ServerState
		"""
		response = await self._client.request(f"{self.method}/status")
		return ServerState(**response)
	
	async def save(self, flush: bool) -> bool:
		"""
		Save server state.

		:param flush: Whether to flush all data to disk.
		:type flush: bool
		"""
		params = {"flush": flush}
		response = await self._client.request(f"{self.method}/save", params=params)
		return response
	
	async def stop(self) -> bool:
		"""
		Stop the server.

		:return: True is the server is stopping.
		:rtype: bool
		"""
		response = await self._client.request(f"{self.method}/stop")
		return response
	
	async def system_message(self, message: SystemMessage) -> bool:
		"""
		Send a system message.

		:param message: The SystemMessage to send.
		:type message: SystemMessage
		:return: True if the message was sent.
		:rtype: bool
		"""
		params = {"message": asdict(message)}
		response = await self._client.request(f"{self.method}/system_message", params=params)
		return response

	@event
	async def started(self) -> None:
		"""Called when the server has started."""

	@event
	async def stopping(self) -> None:
		"""Called when the server is stopping."""

	@event
	async def saving(self) -> None:
		"""Called when the server is saving."""

	@event
	async def saved(self) -> None:
		"""Called when the server has finished saving."""

	@event
	async def heartbeat(self, status: ServerState) -> None:
		"""
		Called when the server status heartbeat is received.

		:param status: The current server status.
		:type status: ServerState
		"""

	@event
	async def activity(self) -> None:
		"""Called when the network connection is initialized."""