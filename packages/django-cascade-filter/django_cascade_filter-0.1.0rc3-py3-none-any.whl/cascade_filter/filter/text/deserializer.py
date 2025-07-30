from cascade_filter.clause import Clause
from cascade_filter.filter.text import TextFilter
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


class TextFilterDeserializer:
	def __init__(self) -> None:
		self.value_deserializer = FilterValueDeserializer[str]()

	def deserialize(self, value: ExpectedValue) -> TextFilter:
		return TextFilter(
			clause=Clause(value["clause"]),
			enabled=value["enabled"],
			table_field=value["tableField"],
			value=self.value_deserializer.deserialize(value["value"]),
		)
