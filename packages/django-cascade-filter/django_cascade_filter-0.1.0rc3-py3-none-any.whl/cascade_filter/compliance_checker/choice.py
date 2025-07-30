from cascade_filter.clause import Clause
from cascade_filter.filter import ChoiceFilter
from cascade_filter.compliance_checker.single import SingleChecker


class Missing:
	pass


class ChoiceChecker(SingleChecker[ChoiceFilter]):
	def is_fit(self, obj: object) -> bool:
		record_attr_value = getattr(obj, self.cascade_filter.table_field, Missing)

		if record_attr_value is Missing:
			return False

		if self.cascade_filter.clause is Clause.EQUAL:
			return record_attr_value in self.cascade_filter.value.value
		elif self.cascade_filter.clause is Clause.NOT_EQUAL:
			return record_attr_value not in self.cascade_filter.value.value

		raise NotImplementedError(f"Unknown choice filter clause: {self.cascade_filter.clause}")
