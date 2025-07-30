from cascade_filter.clause import Clause
from cascade_filter.filter.array.dataclass import ArrayFilter
from cascade_filter.filter.value.deserializer import FilterValueDeserializer

from typing import TypedDict, List, Any


class FilterValueExpectedValue(TypedDict):
	label: str
	value: List[Any]


class ExpectedValue(TypedDict):
	type: str
	subtype: str
	clause: str
	enabled: bool
	tableField: str
	value: FilterValueExpectedValue


class ArrayFilterDeserializer:
	def __init__(self) -> None:
		self.value_deserializer = FilterValueDeserializer[List[Any]]()

	def deserialize(self, value: ExpectedValue) -> ArrayFilter:
		return ArrayFilter(
			clause=Clause(value["clause"]),
			enabled=value["enabled"],
			table_field=value["tableField"],
			value=self.value_deserializer.deserialize(value["value"]),
		)
