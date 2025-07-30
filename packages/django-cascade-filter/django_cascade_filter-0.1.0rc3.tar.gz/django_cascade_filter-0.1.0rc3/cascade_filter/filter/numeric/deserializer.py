from cascade_filter.clause import Clause
from cascade_filter.filter.numeric import NumericFilter
from cascade_filter.filter.value.deserializer import FilterValueDeserializer

from typing import TypedDict


class FilterValueExpectedValue(TypedDict):
	label: str
	value: int


class ExpectedValue(TypedDict):
	type: str
	subtype: str
	clause: str
	enabled: bool
	tableField: str
	value: FilterValueExpectedValue


class NumericFilterDeserializer:
	def __init__(self) -> None:
		self.value_deserializer = FilterValueDeserializer[int]()

	def deserialize(self, value: ExpectedValue) -> NumericFilter:
		return NumericFilter(
			clause=Clause(value["clause"]),
			enabled=value["enabled"],
			table_field=value["tableField"],
			value=self.value_deserializer.deserialize(value["value"]),
		)
