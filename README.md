# MC SMP

[![Version](https://img.shields.io/pypi/v/mcsmp)](https://pypi.org/project/mcsmp/)
![Python](https://img.shields.io/pypi/pyversions/mcsmp)
![MyPy](https://img.shields.io/badge/mypy-checked-blue)
![License](https://img.shields.io/github/license/TechnoBro03/MC-SMP)

An asynchronous Python client for interacting with Minecraft servers using the Minecraft Server Management Protocol (MCSMP) over WebSockets.

# Table of Contents
- [MC SMP](#mc-smp)
- [Table of Contents](#table-of-contents)
- [Features](#features)
- [Installation](#installation)
- [API Reference](#api-reference)
  - [Methods](#methods)
  - [Attributes](#attributes)
  - [Endpoints](#endpoints)
    - [Allow List](#allow-list)
	- [Bans](#bans)
	- [IP Bans](#ip-bans)
	- [Gamerules](#gamerules)
	- [Operators](#operators)
	- [Players](#players)
	- [Server](#server)
	- [Server Settings](#server-settings)
- [Getting Started](#getting-started)
  - [Enable Server Management](#enable-server-management)
  - [Enable TLS](#enable-tls)
  - [Connecting to a Server](#connecting-to-a-server)
  - [Calling Endpoints](#calling-endpoints)
  - [Subscribing to Notifications](#subscribing-to-notifications)
  - [Calling Custom Methods](#calling-custom-methods)
  - [Subscribing to Custom Notifications](#subscribing-to-custom-notifications)
  - [Logging](#logging)

# Features

- **Asynchronous WebSocket Connection**: Provided non-blocking communication with the server.
- **Authentication**: Uses a server secret key system for authorized access.
- **Encrypted Connections (TLS/SSL)**: Supports secure connections with options for certificate verification and hostname checking.
- **Automated API Discovery**: Includes an discover method to automatically retrieve the supported methods and notifications of the target server.
- **Flexible Integration**: Easily implement non-standard protocol features by leveraging the exposed `request()` method and `on_notification` event.
- **Asynchronous Context Manager**: Supports the `async with` pattern for safe connection opening and automatic cleanup.
- **Real-time Notifications**: Provides an event-driven system for responding to server activity.
- **Custom Handlers**: Subscribe to predefined events like `players.joined`, `gamerules.updated`, etc to easily integrate custom logic.
- **Logging**: Built-in logging allows for easy debugging.

# Installation

1. Make sure `pip` is installed on your system.
2. Run the following command
	```bash
	pip install mcsmp
	```
> [!TIP]
> See [here](https://packaging.python.org/en/latest/tutorials/installing-packages/) for more details on installing packages.

# API Reference

## Methods
| Method | Description | Parameters | Return |
| --- | --- | --- | --- |
| \_\_init\_\_() | Initialize a new MC SMP client. | **host**: str, **port**: int, **secret**: str, **tls**: bool, **cert**: str \| None, **check_hostname**: bool, **timeout**: float | None |
| connect() | Connect to the Minecraft server via WebSocket. | None | None |
| close() | Close the WebSocket connection to the Minecraft server. | None | None |
| request() | Send a [JSON-RPC](https://www.jsonrpc.org/specification) request to the server and await the response. | **method**: str, **params**: Any | **Any** |
| discover() | Return an API schema containing supported methods and notifications.| None | **dict[str, Any]** |

## Attributes
| Attribute | Description |
| --- | --- |
| **on_notification**: Event | An event that is invoked when a notification is received from the server. |
| **host**: str | The host/ip address of the server. |
| **port**: int | The port of the server. |
| **tls**: bool | Whether TLS is being used for a secure connection. |

## Endpoints

### Allow List

Endpoints and notifications related to the server allow list (whitelist).\
`client.allow_list.*`

| Endpoint | Description | Parameters | Return |
| --- | --- | --- | --- |
| get() | Get the current allow list. | None | **list[Player]** |
| set() | Set the allow list to the provided list of players. | **players**: list[Player] | **list[Player]** |
| add() | Add players to the allow list. | **players**: list[Player] | **list[Player]** |
| remove() | Remove players from the allow list. | **players**: list[Player] | **list[Player]** |
| clear() | Clear all players from the allow list. | None | **list[Player]** |

| Notification | Description | Event Arguments |
| --- | --- | --- |
| added | Called when a player is added to the allowlist. | **player**: Player |
| removed | Called when a player is removed from the allowlist. | **player**: Player |

### Bans

Endpoints and notifications related to the server ban list.\
`client.bans.*`

| Endpoint | Description | Parameters | Return |
| --- | --- | --- | --- |
| get() | Get the current ban list. | None | **list[UserBad]** |
| set() | Set the ban list to the provided list of players. | **bans**: list[UserBan] | **list[UserBan]** |
| add() | Add players to the ban list. | **bans**: list[UserBan] | **list[UserBan]** |
| remove() | Remove players from the ban list. | **bans**: list[Player] | **list[UserBan]** |
| clear() | Clear all players from the ban list. | None | **list[UserBan]** |

| Notification | Description | Event Arguments |
| --- | --- | --- |
| added | Called when a player is added to the ban list. | **player**: UserBan |
| removed | Called when a player is removed from the ban list. | **player**: Player |

### IP Bans

Endpoints and notifications related to the server IP ban list.\
`client.ip_bans.*`

| Endpoint | Description | Parameters | Return |
| --- | --- | --- | --- |
| get() | Get the current IP ban list. | None | **list[IPBan]** |
| set() | Set the IP ban list to the provided list of players. | **bans**: list[IPBan] | **list[IPBan]** |
| add() | Add players to the IP ban list. | **bans**: list[IncomingIPBan] | **list[IPBan]** |
| remove() | Remove IPs from the IP ban list. | **bans**: list[str] | **list[IPBan]** |
| clear() | Clear all IPs from the IP ban list. | None | **list[IPBan]** |

| Notification | Description | Event Arguments |
| --- | --- | --- |
| added | Called when an IP is added to the ban list. | **player**: IPBan |
| removed | Called when an IP is removed from the ban list. | **player**: str |

### Gamerules

Endpoints and notifications related to the server gamerules.\
`client.gamerules.*`

| Endpoint | Description | Parameters | Return |
| --- | --- | --- | --- |
| get() | Get the available game rules and their current values. | None | **list[TypedGameRule]** |
| update() | Update a gamerule to the provided value. | **gamerule**: UntypedGameRule | **TypedGameRule** |

| Notification | Description | Event Arguments |
| --- | --- | --- |
| updated | Called when a gamerule is updated. | **gamerule**: TypedGameRule |

### Operators

Endpoints and notifications related to the server operators.\
`client.operators.*`

| Endpoint | Description | Parameters | Return |
| --- | --- | --- | --- |
| get() | Get all current operators. | None | **list[Operator]** |
| set() | Set the operators to the provided list. | **operators**: list[Operator] | **list[Operator]** |
| add() | Add players to the operators. | **operators**: list[Operator] | **list[Operator]** |
| remove() | Remove players from the operators. | **operators**: list[Player] | **list[Operator]** |
| clear() | Clear all operators. | None | **list[Operator]** |

| Notification | Description | Event Arguments |
| --- | --- | --- |
| added | Called when an operator is added. | **player**: Operator |
| removed | Called when an operator is removed. | **player**: Operator |

### Players

Endpoints and notifications related to players.\
`client.players.*`

| Endpoint | Description | Parameters | Return |
| --- | --- | --- | --- |
| get() | Get all currently online players. | None | **list[Player]** |
| kick() | Kick players from the server. | **kick**: list[KickPlayer] | **list[Player]** |

| Notification | Description | Event Arguments |
| --- | --- | --- |
| joined | Called when a player joins the server. | **player**: Player |
| left | Called when a player leaves the server. | **player**: Player |

### Server

Endpoints and notifications related to the server.\
`client.server.*`

| Endpoint | Description | Parameters | Return |
| --- | --- | --- | --- |
| status() | Get the server status | None | **ServerState** |
| save() | Save the server. | **flush**: bool | **bool** |
| stop() | Stop the server. | None | **bool** |
| system_message() | Send a system message. | **message**: SystemMessage | **bool** |

| Notification | Description | Event Arguments |
| --- | --- | --- |
| started | Called when the server has started. | None |
| stopping | Called when the server is stopping. | None |
| saving | Called when the server is saving. | None |
| saved | Called whe the server has finished saving. | None|
| heartbeat | Called when the server status heartbeat is received. | **status**: ServerState |
| activity | Called when the network connection is initialized. | None 

### Server Settings

Endpoints and notifications related to the server settings.\
`client.server_settings.*`

| Endpoint | Description | Parameters | Return |
| --- | --- | --- | --- |
| autosave() | Get whether autosave is enabled. | None | **bool** |
| set_autosave() | Set whether autosave is enabled. | **enable**: bool | **bool** |
| difficulty() | Get the current difficulty setting. | None | **Difficulty** |
| set_difficulty() | Set the current difficulty setting. | **difficulty**: Difficulty | **Difficulty** |
| enforce_allowlist() | Get whether allowlist enforcement is enabled. | None | **bool** |
| set_enforce_allowlist() | Set whether allowlist enforcement is enabled. | **enforce**: bool | **bool** |
| use_allowlist() | Get whether the allowlist is being used. | None | **bool** |
| set_use_allowlist() | Set whether the allowlist is being used. | **use**: bool | **bool** |
| max_players() | Get the maximum number of players allowed. | None | **int** |
| set_max_players() | Set the maximum number of players allowed. | **max_players**: int | **int** |
| pause_when_empty_seconds() | Get seconds to wait before pausing when empty. | None | **int** |
| set_pause_when_empty_seconds() | Set seconds to wait before pausing when empty. | **seconds**: int | **int** |
| player_idle_timeout() | Get allowed idle seconds before kick. | None | **int** |
| set_player_idle_timeout() | Set allowed idle seconds before kick. | **seconds**: int | **int** |
| allow_flight() | Get whether flight is allowed in survival. | None | **bool** |
| set_allow_flight() | Set whether flight is allowed in survival. | **allowed**: bool | **bool** |
| motd() | Get the server's message of the day. | None | **str** |
| set_motd() | Set the server's message of the day. | **message**: str | **str** |
| spawn_protection_radius() | Get the spawn protection radius in blocks. | None | **int** |
| set_spawn_protection_radius() | Set the spawn protection radius in blocks. | **radius**: int | **int** |
| force_game_mode() | Get whether default game mode is forced. | None | **bool** |
| set_force_game_mode() | Set whether default game mode is forced. | **force**: bool | **bool** |
| game_mode() | Get the server's default game mode. | None | **GameType** |
| set_game_mode() | Set the server's default game mode. | **mode**: GameType | **GameType** |
| view_distance() | Get the server's view distance in chunks. | None | **int** |
| set_view_distance() | Set the server's view distance in chunks. | **distance**: int | **int** |
| simulation_distance() | Get the server's simulation distance in chunks. | None | **int** |
| set_simulation_distance() | Set the server's simulation distance in chunks. | **distance**: int | **int** |
| accept_transfers() | Get whether to accept transfers from other servers. | None | **bool** |
| set_accept_transfers() | Set whether to accept transfers from other servers. | **accept**: bool | **bool** |
| status_heartbeat_interval() | Get the status heartbeat interval in seconds. | None | **int** |
| set_status_heartbeat_interval() | Set the status heartbeat interval in seconds. | **seconds**: int | **int** |
| operator_user_permission_level() | Get the permission level for operators. | None | **int** |
| set_operator_user_permission_level() | Set the permission level for operators. | **level**: int | **int** |
| hide_online_players() | Get whether online players are hidden in status. | None | **bool** |
| set_hide_online_players() | Set whether online players are hidden in status. | **hide**: bool | **bool** |
| status_replies() | Get whether the server replies to status requests. | None | **bool** |
| set_status_replies() | Set whether the server replies to status requests. | **enable**: bool | **bool** |
| entity_broadcast_range() | Get the entity broadcast range percentage. | None | **int** |
| set_entity_broadcast_range() | Set the entity broadcast range percentage. | **percentage_points**: int | **int** |

# Getting Started

## Enable Server Management
To use the Minecraft Server Management Protocol, it must first be enabled in `server.properties`.

- `management-server-enabled`: Set to true to enable the API.
- `management-server-host`: Host of the API endpoint.
- `management-server-port`: Port of the endpoint. Defaults to 0, assigning a random port on startup. Can be changed to a static port.
- `management-server-secret`: A 40 alphanumeric character secret. The secret will be automatically generated if left empty. Unauthorized requests are rejected with 401 Unauthorized.

> [!Tip]
> For more details about the Minecraft Server Management Protocol, see [here](https://minecraft.wiki/w/Minecraft_Server_Management_Protocol).

## Enable TLS
To use the Minecraft Server Management Protocol over a secure connection (TLS), you must setup a keystore.

> [!NOTE]
> TLS is not required, but is recommended for security.

An example for creating a compatible keystore:

**1. Generate the Keystore**

Use the `keytool` utility to create a PKCS12 keystore (required by Minecraft). This file contains both your private key (which stays on the server) and your public certificate.

```bash
keytool -genkeypair -alias test_key -keyalg RSA -keysize 2048 -storetype PKCS12 \
-keystore test_store.p12 -validity 3650 \
-ext "san=dns:host.name" \
-dname "CN=host.name, OU=MCSMP, O=MC, L=City, ST=State, C=US"
```

- **-genkeypair**: Tells the tool to generate a new public/private key pair.
- **-alias**: A shorthand name for this specific entry in your keystore.
- **-keyalg**: The algorithm used for encryption (**RSA** is the standard choice).
- **-keysize**: The strength of the key; **2048**-bit is highly secure.
- **-storetype**: Format for storing certificates and keys (**PKCS12** is standard and required by Minecraft)
- **-keystore**: The name of the file that will be created (e.g. **test_store.p12**)
- **-validity**: Sets how long the certificate is valid for in days.
- **-ext** "san=dns:...": Adds a Subject Alternative Name. Required if you want to verify the domain name you connect to.
- **-dname**: The "Distinguished Name" which describes the owner (only one is required):
  - **CN** (Common Name): The hostname/domain of your server.
  - **OU** (Organizational Unit): Your department or project name.
  - **O** (Organization): Your company or group name.
  - **L** (Locality): Your city.
  - **ST** (State): Your state or province.
  - **C** (Country): Your two-letter country code (e.g., "US").

**2. Extract the Public Certificate for Clients**

The client needs the Public Certificate to verify the server's identity, but it should never have access to your private key.
Run this command to extract the public .crt file from the keystore you just created:

```bash
keytool -exportcert -alias test_key -keystore test_store.p12 -rfc -file test_cert.crt
```

- **-exportcert**: Tells the tool to extract the public portion of the keypair.
- **-alias**: A shorthand name for the specific cert.
- **-keystore**: The keystore to use (from the above step).
- **-rfc**: Outputs the certificate in a standard text-based format (PEM).
- **-file**: The name of the certificate file to generate.

**3. Modify`server.properties`**

To enable TLS on your server, you'll need to change the following settings:
- `management-server-tls-enabled=true`
- `management-server-tls-keystore=test_store.p12`

You must also set the keystore password in one of three ways:
- Server property: `management-server-tls-keystore-password=...`
- JVM argument: `-Dmanagement.tls.keystore.password=...`
- Environment variable: `MINECRAFT_MANAGEMENT_TLS_KEYSTORE_PASSWORD`

**4. Client Usage**

Although the server now has a certificate, it is not required that the client verify it. Enabling TLS without a certificate will encrypt the communication, but will not necessarily be secure. It is recommended that you always use the public certificate in your client.

```python
from mcsmp import Client

# Pass the path to the .crt file to enable SSL verification
client = Client(host="host.name", port=25585, tls=True, cert="test_cert.crt")
```

## Connecting to a Server

Standard `connect()` and `close()` methods:

```python
import asyncio
from mcsmp.client import Client

async def main():
	client = Client("host.name", 25585, "YOUR_40_CHARACTER_SECRET")
	await client.connect()
	await client.close()

if __name__ == "__main__":
	asyncio.run(main())
```

Using context manager (recommended):

```python
import asyncio
from mcsmp.client import Client

async def main():
	# Automatically connect when entering the scope, and close the connection when leaving the scope
	async with Client("host.name", 25585, "YOUR_40_CHARACTER_SECRET") as client:
		...

if __name__ == "__main__":
	asyncio.run(main())
```

## Calling Endpoints
```python
import asyncio
from mcsmp.client import Client
from mcsmp.schemas import UntypedGameRule

async def main():
	async with Client("host.name", 25585, "YOUR_40_CHARACTER_SECRET") as client:
		# Get the currently online players
		players = await client.players.get()

		# Update gamerule
		updated_rule = await client.gamerules.update(UntypedGameRule(key="advance_time", value=False))
```

## Subscribing to Notifications

```python
import asyncio
from mcsmp.client import Client
from mcsmp.schemas import UntypedGameRule

async def main():
	async with Client("host.name", 25585, "YOUR_40_CHARACTER_SECRET") as client:
		client.gamerules.updated.subscribe(lambda gamerule: print(f"Gamerule updated: {gamerule.key} = {gamerule.value}"))

		updated_rule = await client.gamerules.update(UntypedGameRule(key="advance_time", value=False))

if __name__ == "__main__":
	asyncio.run(main())

# Output:
# Gamerule updated: advance_time = False
```

## Calling Custom Methods

If the server has custom methods, use `request()` directly to call them.

```python
import asyncio
from mcsmp.client import Client

async def main():
	async with Client("host.name", 25585, "YOUR_40_CHARACTER_SECRET") as client:
		result = await client.request(method="namespace:method", params={"param1": "value1"})

if __name__ == "__main__":
	asyncio.run(main())
```

## Subscribing to Custom Notifications

If the server has custom notifications, use `on_notification` to subscribe to them.

```python
import asyncio
from mcsmp.client import Client
from mcsmp.jsonrpc import Request

async def main():
	def custom_handler(notification: Request) -> None:
		if notification.method != "namespace:notification": return # Filter for specific notifications
		print(f"Custom notification: {notification.method} with params: {notification.params}")

	async with Client("host.name", 25585, "YOUR_40_CHARACTER_SECRET") as client:
		client.on_notification.subscribe(custom_handler) # Subscribe custom handler to notifications

if __name__ == "__main__":
	asyncio.run(main())
```

## Logging

```python
import asyncio
import logging

# Enable a basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

async def main():
	client = Client("host.name", 25585, "YOUR_40_CHARACTER_SECRET")
	await client.connect()
	await client.close()

if __name__ == "__main__":
	asyncio.run(main())

# Output
# 2026-01-20 11:13:01 [INFO] mcsmp.client: Connected to ws://host.name:25585.
# 2026-01-20 11:13:02 [INFO] mcsmp.client: Closed connection.
```