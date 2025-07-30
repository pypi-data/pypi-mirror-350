from cascade_filter.filter import BaseFilter
from cascade_filter.field_type import FieldType
from cascade_filter.filter.type import FilterType
from cascade_filter.filter.multi import MultiFilterDeserializer
from cascade_filter.filter.date import DateFilterDeserializer
from cascade_filter.filter.choice import ChoiceFilterDeserializer
from cascade_filter.filter.text import TextFilterDeserializer
from cascade_filter.filter.numeric import NumericFilterDeserializer
from cascade_filter.filter.boolean import BooleanFilterDeserializer
from cascade_filter.filter.array import ArrayFilterDeserializer


def deserialize(raw_filter: dict) -> BaseFilter:
	filter_type = raw_filter.get("type")

	if filter_type == FilterType.SINGLE.value:
		filter_subtype = raw_filter.get("subtype")

		if filter_subtype == FieldType.DATE.value:
			deserializer = DateFilterDeserializer()
		elif filter_subtype == FieldType.CHOICE.value:
			deserializer = ChoiceFilterDeserializer()
		elif filter_subtype == FieldType.TEXT.value:
			deserializer = TextFilterDeserializer()
		elif filter_subtype == FieldType.NUMERIC.value:
			deserializer = NumericFilterDeserializer()
		elif filter_subtype == FieldType.BOOLEAN.value:
			deserializer = BooleanFilterDeserializer()
		elif filter_subtype == FieldType.ARRAY.value:
			deserializer = ArrayFilterDeserializer()
		else:
			raise NotImplementedError(f"Deserialization of filters of subtype \"{filter_subtype}\" is not implemented")

	elif filter_type == FilterType.MULTI.value:
		deserializer = MultiFilterDeserializer()

	else:
		raise NotImplementedError(f"Deserialization of filters of type \"{filter_type}\" is not implemented")

	return deserializer.deserialize(raw_filter)		# type: ignore - Validators must do their job
