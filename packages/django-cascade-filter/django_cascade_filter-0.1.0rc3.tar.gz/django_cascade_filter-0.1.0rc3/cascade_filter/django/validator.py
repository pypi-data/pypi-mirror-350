from cascade_filter.filter.base import BaseFilterValidator
from cascade_filter.filter.single import SingleFilterValidator
from cascade_filter.filter.multi import MultiFilterValidator
from cascade_filter.filter.type import FilterType
from cascade_filter.filter.date import DateFilterValidator
from cascade_filter.filter.choice import ChoiceFilterValidator
from cascade_filter.filter.text import TextFilterValidator
from cascade_filter.filter.numeric import NumericFilterValidator
from cascade_filter.filter.boolean import BooleanFilterValidator
from cascade_filter.filter.array import ArrayFilterValidator
from cascade_filter.exception import ValidationError
from cascade_filter.meta import Table
from cascade_filter.field_type import FieldType

from json import loads
from logging import getLogger; log = getLogger(__name__)
from typing import Type

from django.core.validators import BaseValidator
from django.core.exceptions import ValidationError


class CascadeFilterValidator(BaseValidator):
	def __init__(self, table_meta: Type[Table]) -> None:
		self.table_meta = table_meta

	def __call__(self, value):
		if isinstance(value, str):
			try:
				value = loads(value)
			except Exception as err:
				log.debug(err)
				raise ValidationError("Invalid JSON-format")

		if not isinstance(value, dict):
			raise ValidationError("Value must be valid JSON-object")

		filter_editor_version = value.get("filterEditorVersion")

		if not isinstance(filter_editor_version, int) or filter_editor_version < 1:
			raise ValidationError("The \"filterEditorVersion\" must be positive integer")

		raw_filter = value.get("filter")

		if not isinstance(raw_filter, dict) and raw_filter is not None:
			raise ValidationError("The \"filter\" field value must be valid JSON-object or null")

		if raw_filter is not None:
			filter_validator = BaseFilterValidator()

			try:
				base_cleaned_data = filter_validator.validate(raw_filter)

				if base_cleaned_data["type"] is FilterType.SINGLE:
					single_filter_validator = SingleFilterValidator()
					single_filter_cleaned_data = single_filter_validator.validate(raw_filter)

					if single_filter_cleaned_data["subtype"] is FieldType.DATE:
						validator = DateFilterValidator()
					elif single_filter_cleaned_data["subtype"] is FieldType.CHOICE:
						validator = ChoiceFilterValidator()
					elif single_filter_cleaned_data["subtype"] is FieldType.TEXT:
						validator = TextFilterValidator()
					elif single_filter_cleaned_data["subtype"] is FieldType.NUMERIC:
						validator = NumericFilterValidator()
					elif single_filter_cleaned_data["subtype"] is FieldType.BOOLEAN:
						validator = BooleanFilterValidator()
					elif single_filter_cleaned_data["subtype"] is FieldType.ARRAY:
						validator = ArrayFilterValidator()
					else:
						raise NotImplementedError(
							f"Validation of filters of subtype \"{single_filter_cleaned_data['subtype']}\" is not implemented",
						)

					validator.validate(raw_filter)

				elif base_cleaned_data["type"] is FilterType.MULTI:
					multi_filter_validator = MultiFilterValidator()
					multi_filter_validator.validate(raw_filter)
				else:
					raise NotImplementedError(
						f"Validating filter of type \"{base_cleaned_data['type']}\" is not implemented",
					)

			except ValidationError as err:
				raise ValidationError(*err.args) from err
