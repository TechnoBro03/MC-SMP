import asyncio
import json
import uuid
import ssl
import logging
from types import TracebackType
from typing import Any, AsyncContextManager, Final
from asyncio import Future, Task, Lock
from websockets import connect, ClientConnection
from mcsmp.jsonrpc import Request, Response
from mcsmp.endpoints import *
from pyeventic import event

logger = logging.getLogger("mcsmp.client")

class Client(AsyncContextManager["Client"]):
	"""
	An asynchronous client for interacting with a Minecraft server using the Minecraft Server Management Protocol (MCSMP) over WebSocket.

	See `MC SMP Documentation <https://github.com/TechnoBro03/MC-SMP>`_ for more information.
	"""

	def __init__(self, host: str, port: int, secret: str, *, tls: bool = False, cert: str | None = None, check_hostname: bool = True, timeout: float = 10.0) -> None:
		"""
		Initialize an MCSMP client.

		:param host: The hostname or IP address of the Minecraft server.
		:type host: str
		:param port: The port number of the Minecraft server.
		:type port: int
		:param secret: The secret key for authentication.
		:type secret: str
		:param tls: Whether to use TLS for the connection.
		:type tls: bool
		:param cert: Path to a file of concatenated CA certificates in PEM format for verifying the server's certificate.
		:type cert: str | None
		:param check_hostname: Whether to verify the server's hostname in the TLS certificate.
		:type check_hostname: bool
		:param timeout: The timeout duration for requests in seconds.
		:type timeout: float
		"""
		self.host: Final[str] = host
		self.port: Final[int] = port
		self.tls: Final[bool] = tls or cert is not None

		self._secret: Final[str] = secret
		self._cert: Final[str | None] = cert
		self._check_hostname: Final[bool] = check_hostname
		self._timeout: Final[float] = timeout
		self._lock = Lock()
		self._ws: ClientConnection | None = None
		self._recv_task: Task[None] | None = None

		self._requests: dict[str, Future[Any]] = {}

		# Build endpoints
		self.allow_list = AllowList(self)
		"""The AllowList endpoint for managing the server's allow list."""
		self.bans = Bans(self)
		"""The Bans endpoint for managing player bans."""
		self.gamerules = Gamerules(self)
		"""The Gamerules endpoint for managing server game rules."""
		self.ip_bans = IPBans(self)
		"""The IPBans endpoint for managing IP bans."""
		self.operators = Operators(self)
		"""The Operators endpoint for managing server operators."""
		self.players = Players(self)
		"""The Players endpoint for managing players."""
		self.server_settings = ServerSettings(self)
		"""The ServerSettings endpoint for managing server settings."""
		self.server = Server(self)
		"""The Server endpoint for server-related operations and notifications."""

	async def connect(self) -> None:
		"""
		Connect to the Minecraft server via WebSocket.

		:raises SSLCertVerificationError: If SSL certificate verification fails. The server's certificate may be invalid or untrusted.
		:raises SSLError: If an SSL error occurs.
		:raises ConnectionRefusedError: If the connection is refused. The server may be offline or unreachable.
		:raises RuntimeError: If any other connection error occurs. A 401 error means the provided secret is invalid.
		"""
		if self._ws: return
		header = {
			"Authorization": f"Bearer {self._secret}",
			"Origin": "mcsmp-client"
		}

		if self.tls:
			uri = f"wss://{self.host}:{self.port}" # Secure WebSocket
			ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS) # Does not verify cert or hostname by default
			if self._cert:
				ssl_context.load_verify_locations(cafile=self._cert)
				ssl_context.verify_mode = ssl.CERT_REQUIRED
				ssl_context.check_hostname = self._check_hostname

		else:
			uri = f"ws://{self.host}:{self.port}"
			ssl_context = None

		try:
			self._ws = await connect(uri, additional_headers=header, ssl=ssl_context)
			logger.info(f"Connected to {uri}.")
			self._recv_task = asyncio.create_task(self._recv_loop(), name="mcsmp-jsonrpc-recv")
		except ssl.SSLCertVerificationError as e:
			raise RuntimeError(f"SSL certificate verification failed: {e}") from e
		except ssl.SSLError as e:
			raise RuntimeError(f"SSL error occurred: {e}") from e
		except ConnectionRefusedError as e:
			raise RuntimeError(f"Connection to {uri} was refused: {e}") from e
		except Exception as e:
			raise RuntimeError(f"Failed to connect to {uri}: {e}") from e

	async def close(self) -> None:
		"""Close the WebSocket connection to the Minecraft server."""
		if self._recv_task:
			self._recv_task.cancel()
			try: await self._recv_task
			except asyncio.CancelledError: ...
			finally: self._recv_task = None
			logger.debug("Stopped receive loop.")

		if self._ws:
			try: await self._ws.close()
			finally: self._ws = None
			logger.info("Closed connection.")

		# Wait for all notification handlers to complete
		await self.on_notification.wait()

	async def request(self, method: str, params: Any = None) -> Any:
		"""
		Send a JSON-RPC request to the server and await the response.

		:param method: The JSON-RPC method to call.
		:type method: str
		:param params: The parameters for the JSON-RPC method.
		:type params: Any
		:return: The result of the JSON-RPC call.
		:rtype: Any
		"""
		if not self._ws: raise RuntimeError("WebSocket is not connected.")

		request_id = uuid.uuid4().hex
		request = Request(id=request_id, method=method, params=params)
		logger.debug(f"Sending request: {method} (id: {request_id})")

		future = asyncio.get_running_loop().create_future()
		async with self._lock: self._requests[request_id] = future

		# Wait for response (future will be set in the recv loop)
		try:
			await self._ws.send(json.dumps(dict(request)))
			result = await asyncio.wait_for(future, timeout=self._timeout)
			logger.debug(f"Received response for request: {method} (id: {request_id})")
			return result
		except asyncio.TimeoutError:
			logger.exception(f"Request {method} (id: {request_id}) timed out after {self._timeout} seconds.")
			raise RuntimeError(f"Request {method} timed out after {self._timeout} seconds.")
		except Exception as e:
			logger.exception(f"An error occurred while sending request {method} (id: {request_id}): {e}")
			raise RuntimeError(f"An error occurred while sending request {method}.") from e
		finally:
			async with self._lock: self._requests.pop(request_id, None)

	async def discover(self) -> dict[str, Any]:
		"""
		Returns an API schema containing supported methods and notifications of the currently running server.

		:return: A JSON string representing the API schema.
		:rtype: str
		"""
		if not self._ws: raise RuntimeError("WebSocket is not connected.")

		response = await self.request("rpc.discover")
		return response

	@event
	async def on_notification(self, notification: Request) -> None:
		"""
		Event triggered when a notification is received from the server.

		:param notification: The received JSON-RPC notification.
		:type notification: Request
		"""

	async def _recv_loop(self) -> None:
		if not self._ws: return

		try:
			logger.debug("Starting receive loop...")
			async for message in self._ws:
				try: response: dict[Any, Any] | list[dict[Any, Any]] = json.loads(message)
				except Exception as e:
					logger.error(f"Failed to decode JSON message: {e}")
					continue

				# It's possible JSON RPC messages are sent in batches
				if isinstance(response, list):
					for item in response:
						await self._handle_item(item)
				else:
					await self._handle_item(response)
		except Exception as e:
			logger.exception(f"An error occurred in the receive loop.")
			async with self._lock:
				for future in self._requests.values():
					if not future.done():
						future.set_exception(RuntimeError(f"An error occurred: {e}"))
				self._requests.clear()
		finally:
			await self.close()

	async def _handle_item(self, item: dict[str, Any]):
		try:
			request_id = item.get("id")

			# Response
			if request_id is not None:
				logger.debug(f"Handling response for request id: {request_id}")
				async with self._lock:
					future = self._requests.pop(request_id, None)

				if future and not future.done():
					response = Response(**item)

					if response.error:
						data = f" ({response.error.data})" if response.error.data else ""
						future.set_exception(RuntimeError(f"[{response.error.code}] {response.error.message}{data}"))
					else:
						future.set_result(response.result)

			# Notification
			else:
				logger.debug(f"Handling notification: {item.get('method')}")
				notification = Request(**item)
				self.on_notification.fire(notification) # Schedule notification handlers in background
		except Exception:
			logger.exception(f"An error occurred while handling item.")
			pass

	async def __aenter__(self) -> "Client":
		await self.connect()
		return self
	
	async def __aexit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None) -> None:
		await self.close()
