from cascade_filter.exception import ValidationError

from typing import Any, TypedDict


class CleanedData(TypedDict):
	label: str
	value: Any


class Missing:
	pass


class FilterValueValidator:
	def validate(self, value: Any) -> CleanedData:
		if not isinstance(value, dict):
			raise ValidationError("The filter value must be of dict type")

		filter_label = value.get("label")

		if not isinstance(filter_label, str):
			raise ValidationError("The \"label\" field must be valid string")

		filter_value = value.get("value", Missing)

		if filter_value is Missing:
			raise ValidationError("The \"value\" field is required")

		return CleanedData(label=filter_label, value=filter_value)
