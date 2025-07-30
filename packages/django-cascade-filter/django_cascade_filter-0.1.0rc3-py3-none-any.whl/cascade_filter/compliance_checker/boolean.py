from cascade_filter.clause import Clause
from cascade_filter.filter import BooleanFilter
from cascade_filter.compliance_checker.single import SingleChecker

from typing import cast


class BooleanChecker(SingleChecker[BooleanFilter]):
	def is_fit(self, obj: object) -> bool:
		attr_value = getattr(obj, self.cascade_filter.table_field, None)

		if attr_value is None:
			return False

		attr_value = cast(bool, attr_value)

		if self.cascade_filter.clause is Clause.IS:
			return attr_value == self.cascade_filter.value.value
		elif self.cascade_filter.clause is Clause.IS_NOT:
			return attr_value != self.cascade_filter.value.value

		raise NotImplementedError(f"Unknown boolean filter clause: {self.cascade_filter.clause}")
