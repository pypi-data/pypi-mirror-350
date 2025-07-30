from typing import Any


class Choice:
	__slots__ = "label", "value"

	label: str
	value: Any

	def __init__(self, label: str, value: Any) -> None:
		self.label = label
		self.value = value

	def serialize(self) -> dict:
		return {
			"label": self.label,
			"value": self.value
		}
