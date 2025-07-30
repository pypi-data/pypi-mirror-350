from cascade_filter.exception import ValidationError
from cascade_filter.clause import Clause
from cascade_filter.field_type import FieldType
from cascade_filter.filter.base import BaseFilterValidator
from cascade_filter.filter.base.validator import CleanedData as _CleanedData
from cascade_filter.filter.single import SingleFilterValidator
from cascade_filter.filter.single.validator import CleanedData as SingleFilterCleanedData
from cascade_filter.filter.type import FilterType
from cascade_filter.filter.date import DateFilterValidator
from cascade_filter.filter.choice import ChoiceFilterValidator
from cascade_filter.filter.text import TextFilterValidator
from cascade_filter.filter.numeric import NumericFilterValidator
from cascade_filter.filter.boolean import BooleanFilterValidator
from cascade_filter.filter.array import ArrayFilterValidator

from typing import List, Union, Final, FrozenSet


class CleanedData(_CleanedData):
	subfilters: List[Union["CleanedData", SingleFilterCleanedData]]


class MultiFilterValidator(BaseFilterValidator):
	AVAILABLE_CLAUSES: Final[FrozenSet[Clause]] = frozenset((Clause.AND, Clause.OR))

	def validate(self, value: dict) -> CleanedData:
		base_cleaned_data = super().validate(value)

		if base_cleaned_data["clause"] not in self.AVAILABLE_CLAUSES:
			raise ValidationError("The \"clause\" field must contain one of available clauses")

		filter_subfilters = value.get("subfilters")

		if not isinstance(filter_subfilters, list):
			raise ValidationError("The \"subfilters\" field must contain valid list")

		single_filter_deserializer = SingleFilterValidator()
		subfilters = []

		for subfilter in filter_subfilters:
			if not isinstance(subfilter, dict):
				raise ValidationError("Each subfilter must be of dict type")

			subfilter_type = subfilter.get("type")

			if not FilterType.has_value(subfilter_type):
				raise ValidationError("Each subfilter must have a valid FilterType in the \"type\" field")

			if subfilter_type == FilterType.SINGLE.value:
				single_filter_cleaned_data = single_filter_deserializer.validate(subfilter)

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

				subfilters.append(validator.validate(subfilter))

			elif subfilter_type == FilterType.MULTI.value:
				subfilters.append(self.validate(subfilter))

			else:
				raise NotImplementedError(
					f"Validation of subfilters of type \"{subfilter_type}\" is not implemented",
				)

		return CleanedData(**base_cleaned_data, subfilters=subfilters)
