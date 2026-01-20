from pydantic.dataclasses import dataclass

@dataclass
class IPBan:
	"""An IP ban."""

	reason: str
	"""The reason for the IP ban."""

	expires: str
	"""The expiration date of the IP ban in ISO 8601 format."""

	ip: str
	"""The banned IP address."""

	source: str
	"""The source of the IP ban (e.g., admin, system)."""