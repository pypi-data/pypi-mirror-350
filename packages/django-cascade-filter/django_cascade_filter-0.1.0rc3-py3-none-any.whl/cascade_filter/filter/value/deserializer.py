from cascade_filter.filter.value.dataclass import FilterValue

from typing import TypedDict, TypeVar, Generic, Any


T = TypeVar("T")


class ExpectedValue(TypedDict):
	label: str
	value: Any


class FilterValueDeserializer(Generic[T]):
	def deserialize(self, value: ExpectedValue) -> FilterValue[T]:
		return FilterValue(**value)
