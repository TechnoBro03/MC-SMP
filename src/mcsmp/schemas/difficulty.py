from enum import Enum

class Difficulty(str, Enum):
	"""Minecraft difficulty levels."""

	PEACEFUL = "peaceful"
	"""Peaceful difficulty."""

	EASY = "easy"
	"""Easy difficulty."""

	NORMAL = "normal"
	"""Normal difficulty."""

	HARD = "hard"
	"""Hard difficulty."""