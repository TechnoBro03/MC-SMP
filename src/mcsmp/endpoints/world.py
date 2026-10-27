from typing import TYPE_CHECKING, Awaitable, Callable, Final
from pyeventic import event
from mcsmp.jsonrpc.request import Request
if TYPE_CHECKING:
	from mcsmp.client import Client

class World:
	"""World endpoints."""

	notification: Final[str] = "minecraft:notification/world"

	def __init__(self, client: "Client"):
		self._client = client

		self._endpoints: dict[str, Callable[[Request], Awaitable[None]]] = {
			f"{self.notification}/upgrade_started": lambda n: self.upgrade_started(),
			f"{self.notification}/upgrade_progress": lambda n: self.upgrade_progress(n.params[0]),
			f"{self.notification}/upgrade_finished": lambda n: self.upgrade_finished(),
			f"{self.notification}/upgrade_failed": lambda n: self.upgrade_failed(n.params[0]),
		}
		client.on_notification.subscribe(lambda n: evt(n) if (evt := self._endpoints.get(n.method)) else None) # type: ignore

	@event
	async def upgrade_started(self) -> None:
		"""Called when a world upgrade has started."""

	@event
	async def upgrade_progress(self, progress: float) -> None:
		"""
		Called when world upgrade progress is reported. Rate limited by the server to 1 notification per second.

		:param progress: The upgrade progress, between 0 and 1.
		:type progress: float
		"""

	@event
	async def upgrade_finished(self) -> None:
		"""Called when a world upgrade has finished."""

	@event
	async def upgrade_failed(self, reason: str) -> None:
		"""
		Called when a world upgrade has failed.

		:param reason: The reason the upgrade failed.
		:type reason: str
		"""
