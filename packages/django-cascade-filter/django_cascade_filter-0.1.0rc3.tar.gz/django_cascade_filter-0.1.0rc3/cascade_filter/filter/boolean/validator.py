from cascade_filter.clause import Clause, CLAUSES_ACCORDANCE
from cascade_filter.exception import ValidationError
from cascade_filter.filter.single.validator import SingleFilterValidator, CleanedData as _CleanedData
from cascade_filter.filter.value.validator import CleanedData as _FilterValueCleanedData

from typing import Final, FrozenSet


class FilterValueCleanedData(_FilterValueCleanedData):
	value: bool


class CleanedData(_CleanedData):
	value: FilterValueCleanedData


class BooleanFilterValidator(SingleFilterValidator):
	AVAILABLE_CLAUSES: Final[FrozenSet[Clause]] = frozenset(CLAUSES_ACCORDANCE)

	def validate(self, value: dict) -> CleanedData:
		base_cleaned_data = super().validate(value)

		if base_cleaned_data["clause"] not in self.AVAILABLE_CLAUSES:
			raise ValidationError("The \"clause\" field must contain one of available clauses")

		if not isinstance(base_cleaned_data["value"]["value"], bool):
			raise ValidationError("The \"value\" must be a valid boolean value")

		return base_cleaned_data
