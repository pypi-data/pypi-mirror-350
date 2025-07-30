from cascade_filter.clause import Clause
from cascade_filter.filter.date import DateFilter
from cascade_filter.filter.value.deserializer import FilterValueDeserializer

from typing import TypedDict


class FilterValueExpectedValue(TypedDict):
	label: str
	value: str


class ExpectedValue(TypedDict):
	type: str
	subtype: str
	clause: str
	enabled: bool
	tableField: str
	value: FilterValueExpectedValue


class DateFilterDeserializer:
	def __init__(self) -> None:
		self.value_deserializer = FilterValueDeserializer[str]()

	def deserialize(self, value: ExpectedValue) -> DateFilter:
		return DateFilter(
			clause=Clause(value["clause"]),
			enabled=value["enabled"],
			table_field=value["tableField"],
			value=self.value_deserializer.deserialize(value["value"]),
		)
