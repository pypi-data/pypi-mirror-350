from cascade_filter.clause import Clause
from cascade_filter.filter import DateFilter
from cascade_filter.compliance_checker.single import SingleChecker

from arrow import get as get_arrow


class DateChecker(SingleChecker[DateFilter]):
	def is_fit(self, obj: object) -> bool:
		attr_value = getattr(obj, self.cascade_filter.table_field, None)

		if attr_value is None:
			return False

		attr_value = get_arrow(attr_value)
		filter_value = get_arrow(self.cascade_filter.value.value)

		if self.cascade_filter.clause is Clause.EQUAL:
			return attr_value.date() == filter_value.date()
		elif self.cascade_filter.clause is Clause.NOT_EQUAL:
			return attr_value.date() != filter_value.date()
		elif self.cascade_filter.clause is Clause.GREATER_THAN:
			return attr_value.date() > filter_value.date()
		elif self.cascade_filter.clause is Clause.LESS_THAN:
			return attr_value.date() < filter_value.date()
		elif self.cascade_filter.clause is Clause.GREATER_THAN_OR_EQUAL:
			return attr_value.date() >= filter_value.date()
		elif self.cascade_filter.clause is Clause.LESS_THAN_OR_EQUAL:
			return attr_value.date() <= filter_value.date()

		raise NotImplementedError(f"Unknown date filter clause: {self.cascade_filter.clause}")
