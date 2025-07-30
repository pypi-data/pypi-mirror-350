from cascade_filter.clause import Clause
from cascade_filter.filter.boolean.dataclass import BooleanFilter
from cascade_filter.filter.value.deserializer import FilterValueDeserializer

from typing import TypedDict


class FilterValueExpectedValue(TypedDict):
	label: str
	value: bool


class ExpectedValue(TypedDict):
	type: str
	subtype: str
	clause: str
	enabled: bool
	tableField: str
	value: FilterValueExpectedValue


class BooleanFilterDeserializer:
	def __init__(self) -> None:
		self.value_deserializer = FilterValueDeserializer[bool]()

	def deserialize(self, value: ExpectedValue) -> BooleanFilter:
		return BooleanFilter(
			clause=Clause(value["clause"]),
			enabled=value["enabled"],
			table_field=value["tableField"],
			value=self.value_deserializer.deserialize(value["value"]),
		)
