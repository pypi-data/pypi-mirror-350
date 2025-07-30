from cascade_filter.clause import Clause
from cascade_filter.filter import ArrayFilter
from cascade_filter.compliance_checker.single import SingleChecker


class ArrayChecker(SingleChecker[ArrayFilter]):
	def is_fit(self, obj: object) -> bool:
		attr_value = getattr(obj, self.cascade_filter.table_field, None)

		if attr_value is None:
			return False

		if self.cascade_filter.clause is Clause.CONTAINS:
			return set(attr_value).issuperset(set(self.cascade_filter.value.value))
		elif self.cascade_filter.clause is Clause.NOT_CONTAINS:
			return set(attr_value).isdisjoint(set(self.cascade_filter.value.value))

		raise NotImplementedError(f"Unknown array filter clause: {self.cascade_filter.clause}")
