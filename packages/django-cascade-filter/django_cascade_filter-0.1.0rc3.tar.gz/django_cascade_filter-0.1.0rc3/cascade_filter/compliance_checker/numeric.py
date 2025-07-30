from cascade_filter.clause import Clause
from cascade_filter.filter import NumericFilter
from cascade_filter.compliance_checker.single import SingleChecker

from typing import cast


class NumericChecker(SingleChecker[NumericFilter]):
	def is_fit(self, obj: object) -> bool:
		attr_value = getattr(obj, self.cascade_filter.table_field, None)

		if attr_value is None:
			return False

		attr_value = cast(int, attr_value)

		if self.cascade_filter.clause is Clause.EQUAL:
			return attr_value == self.cascade_filter.value.value
		elif self.cascade_filter.clause is Clause.NOT_EQUAL:
			return attr_value != self.cascade_filter.value.value
		elif self.cascade_filter.clause is Clause.GREATER_THAN:
			return attr_value > self.cascade_filter.value.value
		elif self.cascade_filter.clause is Clause.LESS_THAN:
			return attr_value < self.cascade_filter.value.value
		elif self.cascade_filter.clause is Clause.GREATER_THAN_OR_EQUAL:
			return attr_value >= self.cascade_filter.value.value
		elif self.cascade_filter.clause is Clause.LESS_THAN_OR_EQUAL:
			return attr_value <= self.cascade_filter.value.value

		raise NotImplementedError(f"Unknown number filter clause: {self.cascade_filter.clause}")
