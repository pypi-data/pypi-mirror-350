from typing import Any, Generic, TypeVar


T = TypeVar("T", bound=Any)


class FilterValue(Generic[T]):
	__slots__ = "label", "value"

	label: str
	value: T

	def __init__(self, label: str, value: T) -> None:
		self.label = label
		self.value = value

	def serialize(self) -> dict:
		return {
			"label": self.label,
			"value": self.value,
		}
