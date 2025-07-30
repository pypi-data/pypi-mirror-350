from cascade_filter.clause import Clause
from cascade_filter.field_type import FieldType
from cascade_filter.filter.type import FilterType
from cascade_filter.filter.multi.dataclass import MultiFilter
from cascade_filter.filter.value.deserializer import ExpectedValue as FilterValueExpectedValue
from cascade_filter.filter.date import DateFilterDeserializer
from cascade_filter.filter.choice import ChoiceFilterDeserializer
from cascade_filter.filter.text import TextFilterDeserializer
from cascade_filter.filter.numeric import NumericFilterDeserializer
from cascade_filter.filter.boolean import BooleanFilterDeserializer
from cascade_filter.filter.array import ArrayFilterDeserializer

from typing import TypedDict, List, Union, cast


class ExpectedSingleFilterValue(TypedDict):
	type: str
	subtype: str
	clause: str
	enabled: bool
	table_field: str
	value: FilterValueExpectedValue


class ExpectedValue(TypedDict):
	type: str
	clause: str
	enabled: bool
	subfilters: List[Union["ExpectedValue", ExpectedSingleFilterValue]]


class MultiFilterDeserializer:
	def __init__(self) -> None:
		pass

	def deserialize(self, value: ExpectedValue) -> MultiFilter:
		deserialized_subfilters = []

		for subfilter in value["subfilters"]:
			if subfilter["type"] == FilterType.SINGLE.value:
				subfilter = cast(ExpectedSingleFilterValue, subfilter)
				subfilter_subtype = subfilter["subtype"]

				if subfilter_subtype == FieldType.DATE.value:
					deserializer = DateFilterDeserializer()
				elif subfilter_subtype == FieldType.CHOICE.value:
					deserializer = ChoiceFilterDeserializer()
				elif subfilter_subtype == FieldType.TEXT.value:
					deserializer = TextFilterDeserializer()
				elif subfilter_subtype == FieldType.NUMERIC.value:
					deserializer = NumericFilterDeserializer()
				elif subfilter_subtype == FieldType.BOOLEAN.value:
					deserializer = BooleanFilterDeserializer()
				elif subfilter_subtype == FieldType.ARRAY.value:
					deserializer = ArrayFilterDeserializer()
				else:
					raise NotImplementedError(
						f"Deserialization of subfilters of subtype \"{subfilter['subtype']}\" is not implemented",
					)

				deserialized_subfilters.append(deserializer.deserialize(subfilter))

			elif subfilter["type"] == FilterType.MULTI.value:
				subfilter = cast(ExpectedValue, subfilter)
				deserialized_subfilters.append(self.deserialize(subfilter))

			else:
				raise NotImplementedError(
					f"Deserialization of subfilters of type \"{subfilter['type']}\" is not implemented",
				)

		return MultiFilter(
			clause=Clause(value["clause"]),
			enabled=value["enabled"],
			subfilters=deserialized_subfilters,
		)
