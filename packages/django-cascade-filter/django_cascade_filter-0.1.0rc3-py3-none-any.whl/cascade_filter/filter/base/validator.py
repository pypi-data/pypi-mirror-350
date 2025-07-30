from cascade_filter.clause import Clause
from cascade_filter.exception import ValidationError
from cascade_filter.filter.type import FilterType

from typing import TypedDict


class CleanedData(TypedDict):
	clause: Clause
	enabled: bool
	type: FilterType


class BaseFilterValidator:
	def validate(self, value: dict) -> CleanedData:
		filter_clause = value.get("clause")

		if not Clause.has_value(filter_clause):
			raise ValidationError("The \"clause\" field must contain a valid Clause")

		filter_enabled = value.get("enabled")

		if not isinstance(filter_enabled, bool):
			raise ValidationError("The \"enabled\" field must contain a valid bool")

		filter_type = value.get("type")

		if not FilterType.has_value(filter_type):
			raise ValidationError("The \"enabled\" field must contain a valid FilterType")

		return CleanedData(clause=Clause(filter_clause), enabled=filter_enabled, type=FilterType(filter_type))
