from cascade_filter.field_type import FieldType
from cascade_filter.exception import ValidationError
from cascade_filter.filter.value import FilterValueValidator
from cascade_filter.filter.value.validator import CleanedData as FilterValueCleanedData
from cascade_filter.filter.base import BaseFilterValidator
from cascade_filter.filter.base.validator import CleanedData as _CleanedData


class CleanedData(_CleanedData):
	subtype: FieldType
	table_field: str
	value: FilterValueCleanedData


class SingleFilterValidator(BaseFilterValidator):
	def validate(self, value: dict) -> CleanedData:
		base_cleaned_data = super().validate(value)
		filter_subtype = value.get("subtype")

		if not FieldType.has_value(filter_subtype):
			raise ValidationError("The \"clause\" field must contain a valid FieldType")

		filter_table_field = value.get("tableField")

		if not isinstance(filter_table_field, str):
			raise ValidationError("The \"tableField\" field must contain a valid string")

		filter_raw_value = value.get("value")
		filter_value_deserializer = FilterValueValidator()
		filter_value = filter_value_deserializer.validate(filter_raw_value)

		return CleanedData(
			**base_cleaned_data,
			subtype=FieldType(filter_subtype),
			table_field=filter_table_field,
			value=filter_value,
		)
