from enum import Enum

class GameType(str, Enum):
	"""Minecraft game modes."""

	SURVIVAL = "survival"
	"""Survival mode."""

	CREATIVE = "creative"
	"""Creative mode."""

	ADVENTURE = "adventure"
	"""Adventure mode."""

	SPECTATOR = "spectator"
	"""Spectator mode."""