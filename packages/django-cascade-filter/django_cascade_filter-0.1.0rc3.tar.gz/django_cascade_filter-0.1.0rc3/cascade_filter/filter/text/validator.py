from cascade_filter.clause import Clause, CLAUSES_STRICT_COMPARISON, CLAUSES_CONTAINING, CLAUSES_BOUNDARY
from cascade_filter.exception import ValidationError
from cascade_filter.filter.single.validator import SingleFilterValidator, CleanedData as _CleanedData
from cascade_filter.filter.value.validator import CleanedData as _FilterValueCleanedData

from typing import Final, FrozenSet


class FilterValueCleanedData(_FilterValueCleanedData):
	value: str


class CleanedData(_CleanedData):
	value: FilterValueCleanedData


class TextFilterValidator(SingleFilterValidator):
	AVAILABLE_CLAUSES: Final[FrozenSet[Clause]] = frozenset((
		*CLAUSES_STRICT_COMPARISON, *CLAUSES_CONTAINING, *CLAUSES_BOUNDARY,
	))

	def validate(self, value: dict) -> CleanedData:
		base_cleaned_data = super().validate(value)

		if base_cleaned_data["clause"] not in self.AVAILABLE_CLAUSES:
			raise ValidationError("The \"clause\" field must contain one of available clauses")

		if not isinstance(base_cleaned_data["value"]["value"], str):
			raise ValidationError("The \"value\" must be a valid string")

		return base_cleaned_data
