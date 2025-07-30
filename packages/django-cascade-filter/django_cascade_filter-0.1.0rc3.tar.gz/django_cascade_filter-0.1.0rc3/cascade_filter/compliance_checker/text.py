from cascade_filter.clause import Clause
from cascade_filter.filter import TextFilter
from cascade_filter.compliance_checker.single import SingleChecker

from typing import cast


class TextChecker(SingleChecker[TextFilter]):
	def is_fit(self, obj: object) -> bool:
		attr_value = getattr(obj, self.cascade_filter.table_field, None)

		if attr_value is None:
			return False

		attr_value = cast(str, attr_value)

		if self.cascade_filter.clause is Clause.EQUAL:
			return attr_value == self.cascade_filter.value.value
		elif self.cascade_filter.clause is Clause.NOT_EQUAL:
			return attr_value != self.cascade_filter.value.value
		elif self.cascade_filter.clause is Clause.CONTAINS:
			return self.cascade_filter.value.value in attr_value
		elif self.cascade_filter.clause is Clause.NOT_CONTAINS:
			return self.cascade_filter.value.value not in attr_value
		elif self.cascade_filter.clause is Clause.STARTS_WITH:
			return attr_value.startswith(self.cascade_filter.value.value)
		elif self.cascade_filter.clause is Clause.ENDS_WITH:
			return attr_value.endswith(self.cascade_filter.value.value)

		raise NotImplementedError(f"Unknown text filter clause: {self.cascade_filter.clause}")
