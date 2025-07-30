from cascade_filter.clause import Clause, CLAUSES_CONTAINING
from cascade_filter.exception import ValidationError
from cascade_filter.filter.single.validator import SingleFilterValidator, CleanedData as _CleanedData
from cascade_filter.filter.value.validator import CleanedData as _FilterValueCleanedData

from typing import Final, FrozenSet, List, Any


class FilterValueCleanedData(_FilterValueCleanedData):
	value: List[Any]


class CleanedData(_CleanedData):
	value: FilterValueCleanedData


class ArrayFilterValidator(SingleFilterValidator):
	AVAILABLE_CLAUSES: Final[FrozenSet[Clause]] = frozenset(CLAUSES_CONTAINING)

	def value(self, value: dict) -> CleanedData:
		base_cleaned_data = super().validate(value)

		if base_cleaned_data["clause"] not in self.AVAILABLE_CLAUSES:
			raise ValidationError("The \"clause\" field must contain one of available clauses")

		if not isinstance(base_cleaned_data["value"]["value"], list):
			raise ValidationError("The \"value\" must be of list type")

		return base_cleaned_data
