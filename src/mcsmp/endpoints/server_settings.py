from typing import TYPE_CHECKING, Final
from mcsmp.schemas import Difficulty, GameType
if TYPE_CHECKING:
	from mcsmp.client import Client

class ServerSettings:
	"""Server setting endpoints."""

	endpoint: Final[str] = "minecraft:serversettings"

	def __init__(self, client: "Client"):
		self._client = client

	# /autosave
	async def autosave(self) -> bool:
		"""
		Get whether autosave is enabled.

		:return: True if autosave is enabled.
		:rtype: bool
		"""
		response = await self._client.request(f"{self.endpoint}/autosave")
		return response

	async def set_autosave(self, enable: bool) -> bool:
		"""
		Set whether autosave is enabled.

		:param enable: True to enable autosave, False to disable.
		:type enable: bool
		"""
		params = {"enable": enable}
		response = await self._client.request(f"{self.endpoint}/autosave/set", params=params)
		return response

	# /difficulty
	async def difficulty(self) -> Difficulty:
		"""
		Get the current difficulty setting.

		:return: The current difficulty.
		:rtype: Difficulty
		"""
		response = await self._client.request(f"{self.endpoint}/difficulty")
		return Difficulty(**response)

	async def set_difficulty(self, difficulty: Difficulty) -> Difficulty:
		"""
		Set the current difficulty setting.

		:param difficulty: The difficulty to set.
		:type difficulty: Difficulty
		:return: The updated difficulty.
		:rtype: Difficulty
		"""
		params = {"difficulty": difficulty}
		response = await self._client.request(f"{self.endpoint}/difficulty/set", params=params)
		return Difficulty(**response)

	# /enforce_allowlist
	async def enforce_allowlist(self) -> bool:
		"""
		Get whether allowlist enforcement is enabled (kicks players immediately when removed from the allowlist).

		:return: True if allowlist enforcement is enabled.
		:rtype: bool
		"""
		response = await self._client.request(f"{self.endpoint}/enforce_allowlist")
		return response

	async def set_enforce_allowlist(self, enforce: bool) -> bool:
		"""
		Set whether allowlist enforcement is enabled (kicks players immediately when removed from the allowlist).

		:param enforce: True to enable allowlist enforcement, False to disable.
		:type enforce: bool
		:return: The updated allowlist enforcement setting.
		:rtype: bool
		"""
		params = {"enforce": enforce}
		response = await self._client.request(f"{self.endpoint}/enforce_allowlist/set", params=params)
		return response

	# /use_allowlist
	async def use_allowlist(self) -> bool:
		"""
		Get whether the allowlist is being used.

		:return: True if the allowlist is being used.
		:rtype: bool
		"""
		response = await self._client.request(f"{self.endpoint}/use_allowlist")
		return response

	async def set_use_allowlist(self, use: bool) -> bool:
		"""
		Set whether the allowlist is being used (controls whether only allowlisted players can join).

		:param use: True to use the allowlist, False to disable.
		:type use: bool
		:return: The updated use allowlist setting.
		:rtype: bool
		"""
		params = {"use": use}
		response = await self._client.request(f"{self.endpoint}/use_allowlist/set", params=params)
		return response

	# /max_players
	async def max_players(self) -> int:
		"""
		Get the maximum number of players allowed on the server.

		:return: The maximum number of players.
		:rtype: int
		"""
		response = await self._client.request(f"{self.endpoint}/max_players")
		return response

	async def set_max_players(self, max_players: int) -> int:
		"""
		Set the maximum number of players allowed on the server.

		:param max_players: The maximum number of players to set.
		:type max_players: int
		:return: The updated maximum number of players.
		:rtype: int
		"""
		params = {"max": max_players}
		response = await self._client.request(f"{self.endpoint}/max_players/set", params=params)
		return response

	# /pause_when_empty_seconds
	async def pause_when_empty_seconds(self) -> int:
		"""
		Get the number of seconds the server will wait before pausing when empty.

		:return: The number of seconds before the server pauses when empty.
		:rtype: int
		"""
		response = await self._client.request(f"{self.endpoint}/pause_when_empty_seconds")
		return response

	async def set_pause_when_empty_seconds(self, seconds: int) -> int:
		"""
		Set the number of seconds the server will wait before pausing when empty.

		:param seconds: The number of seconds to set.
		:type seconds: int
		:return: The updated number of seconds before the server pauses when empty.
		:rtype: int
		"""
		params = {"seconds": seconds}
		response = await self._client.request(f"{self.endpoint}/pause_when_empty_seconds/set", params=params)
		return response

	# /player_idle_timeout
	async def player_idle_timeout(self) -> int:
		"""
		Get the number of seconds a player can be idle before being kicked.

		:return: The number of seconds before a player is kicked for idling.
		:rtype: int
		"""
		response = await self._client.request(f"{self.endpoint}/player_idle_timeout")
		return response

	async def set_player_idle_timeout(self, seconds: int) -> int:
		"""
		Set the number of seconds a player can be idle before being kicked.
		:param seconds: The number of seconds to set.
		:type seconds: int
		:return: The updated number of seconds before a player is kicked for idling.
		:rtype: int
		"""
		params = {"seconds": seconds}
		response = await self._client.request(f"{self.endpoint}/player_idle_timeout/set", params=params)
		return response

	# /allow_flight
	async def allow_flight(self) -> bool:
		"""
		Get whether flight is allowed for players in survival mode.

		:return: True if flight is allowed.
		:rtype: bool
		"""
		response = await self._client.request(f"{self.endpoint}/allow_flight")
		return response

	async def set_allow_flight(self, allowed: bool) -> bool:
		"""
		Set whether flight is allowed for players in survival mode.

		:param allowed: True to allow flight, False to disallow.
		:type allowed: bool
		:return: The updated allow flight setting.
		:rtype: bool
		"""
		params = {"allowed": allowed}
		response = await self._client.request(f"{self.endpoint}/allow_flight/set", params=params)
		return response

	# /motd
	async def motd(self) -> str:
		"""
		Get the server's message of the day (MOTD).

		:return: The server MOTD.
		:rtype: str
		"""
		response = await self._client.request(f"{self.endpoint}/motd")
		return response

	async def set_motd(self, message: str) -> str:
		"""
		Set the server's message of the day (MOTD).

		:param message: The message to set as the MOTD.
		:type message: str
		:return: The updated server MOTD.
		:rtype: str
		"""
		params = {"message": message}
		response = await self._client.request(f"{self.endpoint}/motd/set", params=params)
		return response

	# /spawn_protection_radius
	async def spawn_protection_radius(self) -> int:
		"""
		Get the spawn protection radius in blocks (only operators can edit within this radius).

		:return: The spawn protection radius in blocks.
		:rtype: int
		"""
		response = await self._client.request(f"{self.endpoint}/spawn_protection_radius")
		return response

	async def set_spawn_protection_radius(self, radius: int) -> int:
		"""
		Set the spawn protection radius in blocks (only operators can edit within this radius).

		:param radius: The radius in blocks to set.
		:type radius: int
		:return: The updated spawn protection radius in blocks.
		:rtype: int
		"""
		params = {"radius": radius}
		response = await self._client.request(f"{self.endpoint}/spawn_protection_radius/set", params=params)
		return response

	# /force_game_mode
	async def force_game_mode(self) -> bool:
		"""
		Get whether players are forced to use the server's default game mode.

		:return: True if the game mode is forced.
		:rtype: bool
		"""
		response = await self._client.request(f"{self.endpoint}/force_game_mode")
		return response

	async def set_force_game_mode(self, force: bool) -> bool:
		"""
		Set whether players are forced to use the server's default game mode.

		:param force: True to force the game mode, False to disable.
		:type force: bool
		:return: The updated force game mode setting.
		:rtype: bool
		"""
		params = {"force": force}
		response = await self._client.request(f"{self.endpoint}/force_game_mode/set", params=params)
		return response

	# /game_mode
	async def game_mode(self) -> GameType:
		"""
		Get the server's default game mode.

		:return: The server's default game mode.
		:rtype: GameType
		"""
		response = await self._client.request(f"{self.endpoint}/game_mode")
		return GameType(**response)

	async def set_game_mode(self, mode: GameType) -> GameType:
		"""
		Set the server's default game mode.

		:param mode: The game mode to set.
		:type mode: GameType
		:return: The updated server's default game mode.
		:rtype: GameType
		"""
		params = {"mode": mode}
		response = await self._client.request(f"{self.endpoint}/game_mode/set", params=params)
		return GameType(**response)

	# /view_distance
	async def view_distance(self) -> int:
		"""
		Get the server's view distance in chunks.

		:return: The server's view distance in chunks.
		:rtype: int
		"""
		response = await self._client.request(f"{self.endpoint}/view_distance")
		return response

	async def set_view_distance(self, distance: int) -> int:
		"""
		Set the server's view distance in chunks.

		:param distance: The view distance in chunks to set.
		:type distance: int
		:return: The updated server's view distance in chunks.
		:rtype: int
		"""
		params = {"distance": distance}
		response = await self._client.request(f"{self.endpoint}/view_distance/set", params=params)
		return response

	# /simulation_distance
	async def simulation_distance(self) -> int:
		"""
		Get the server's simulation distance in chunks.

		:return: The server's simulation distance in chunks.
		:rtype: int
		"""
		response = await self._client.request(f"{self.endpoint}/simulation_distance")
		return response

	async def set_simulation_distance(self, distance: int) -> int:
		"""
		Set the server's simulation distance in chunks.

		:param distance: The simulation distance in chunks to set.
		:type distance: int
		:return: The updated server's simulation distance in chunks.
		:rtype: int
		"""
		params = {"distance": distance}
		response = await self._client.request(f"{self.endpoint}/simulation_distance/set", params=params)
		return response

	# /accept_transfers
	async def accept_transfers(self) -> bool:
		"""
		Get whether the server accepts player transfers from other servers.

		:return: True if the server accepts player transfers.
		:rtype: bool
		"""
		response = await self._client.request(f"{self.endpoint}/accept_transfers")
		return response

	async def set_accept_transfers(self, accept: bool) -> bool:
		"""
		Set whether the server accepts player transfers from other servers.

		:param accept: True to accept player transfers, False to disable.
		:type accept: bool
		:return: The updated accept transfers setting.
		:rtype: bool
		"""
		params = {"accept": accept}
		response = await self._client.request(f"{self.endpoint}/accept_transfers/set", params=params)
		return response

	# /status_heartbeat_interval
	async def status_heartbeat_interval(self) -> int:
		"""
		Get the interval in seconds between server status heartbeats.

		:return: The interval in seconds between server status heartbeats.
		:rtype: int
		"""
		response = await self._client.request(f"{self.endpoint}/status_heartbeat_interval")
		return response

	async def set_status_heartbeat_interval(self, seconds: int) -> int:
		"""
		Set the interval in seconds between server status heartbeats.

		:param seconds: The interval in seconds to set.
		:type seconds: int
		:return: The updated interval in seconds between server status heartbeats.
		:rtype: int
		"""
		params = {"seconds": seconds}
		response = await self._client.request(f"{self.endpoint}/status_heartbeat_interval/set", params=params)
		return response

	# /operator_user_permission_level
	async def operator_user_permission_level(self) -> int:
		"""
		Get the permissions level required for operator commands.

		:return: The permissions level required for operator commands.
		:rtype: int
		"""
		response = await self._client.request(f"{self.endpoint}/operator_user_permission_level")
		return response

	async def set_operator_user_permission_level(self, level: int) -> int:
		"""
		Set the permissions level required for operator commands.

		:param level: The permissions level to set.
		:type level: int
		:return: The updated permissions level required for operator commands.
		:rtype: int
		"""
		params = {"level": level}
		response = await self._client.request(f"{self.endpoint}/operator_user_permission_level/set", params=params)
		return response

	# /hide_online_players
	async def hide_online_players(self) -> bool:
		"""
		Get whether the server hides online player information from status queries.

		:return: True if online player information is hidden.
		:rtype: bool
		"""
		response = await self._client.request(f"{self.endpoint}/hide_online_players")
		return response

	async def set_hide_online_players(self, hide: bool) -> bool:
		"""
		Set whether the server hides online player information from status queries.

		:param hide: True to hide online player information, False to disable.
		:type hide: bool
		:return: The updated hide online players setting.
		:rtype: bool
		"""
		params = {"hide": hide}
		response = await self._client.request(f"{self.endpoint}/hide_online_players/set", params=params)
		return response

	# /status_replies
	async def status_replies(self) -> bool:
		"""
		Get whether the server responds to connection status requests.

		:return: True if the server responds to status requests.
		:rtype: bool
		"""
		response = await self._client.request(f"{self.endpoint}/status_replies")
		return response

	async def set_status_replies(self, enable: bool) -> bool:
		"""
		Set whether the server responds to connection status requests.

		:param enable: True to enable status replies, False to disable.
		:type enable: bool
		:return: The updated status replies setting.
		:rtype: bool
		"""
		params = {"enable": enable}
		response = await self._client.request(f"{self.endpoint}/status_replies/set", params=params)
		return response

	# /entity_broadcast_range
	async def entity_broadcast_range(self) -> int:
		"""
		Get the entity broadcast range as a percentage.

		:return: The entity broadcast range as a percentage.
		:rtype: int
		"""
		response = await self._client.request(f"{self.endpoint}/entity_broadcast_range")
		return response

	async def set_entity_broadcast_range(self, percentage_points: int) -> int:
		"""
		Set the entity broadcast range as a percentage.

		:param percentage_points: The entity broadcast range to set as a percentage.
		:type percentage_points: int
		:return: The updated entity broadcast range as a percentage.
		:rtype: int
		"""
		params = {"percentage_points": percentage_points}
		response = await self._client.request(f"{self.endpoint}/entity_broadcast_range/set", params=params)
		return response