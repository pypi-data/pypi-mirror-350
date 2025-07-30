from cascade_filter.clause import Clause, CLAUSES_STRICT_COMPARISON, CLAUSES_NON_STRICT_COMPARISON
from cascade_filter.exception import ValidationError
from cascade_filter.filter.single.validator import SingleFilterValidator, CleanedData as _CleanedData
from cascade_filter.filter.value.validator import CleanedData as _FilterValueCleanedData

from typing import Final, FrozenSet
from re import Pattern, compile


class FilterValueCleanedData(_FilterValueCleanedData):
	value: str


class CleanedData(_CleanedData):
	value: FilterValueCleanedData


class DateFilterValidator(SingleFilterValidator):
	DATE_RE: Pattern = compile(r"\d\d\d\d-\d\d-\d\d")
	AVAILABLE_CLAUSES: Final[FrozenSet[Clause]] = frozenset((
		*CLAUSES_STRICT_COMPARISON, *CLAUSES_NON_STRICT_COMPARISON,
	))

	def validate(self, value: dict) -> CleanedData:
		base_cleaned_data = super().validate(value)

		if base_cleaned_data["clause"] not in self.AVAILABLE_CLAUSES:
			raise ValidationError("The \"clause\" field must contain one of available clauses")

		filter_value = base_cleaned_data["value"]["value"]

		if not isinstance(filter_value, str) or not self.DATE_RE.match(filter_value):
			raise ValidationError("The \"value\" must be a valid string in format YYYY-MM-DD")

		return base_cleaned_data
