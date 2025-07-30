from cascade_filter.filter import NumericFilter
from cascade_filter.clause import Clause

from django.db.models.query import Q


class NumericFilterMixin:
	def make_numeric_filter(self, numeric_filter: NumericFilter) -> Q:
		if numeric_filter.clause is Clause.EQUAL:
			return Q(**{numeric_filter.table_field: numeric_filter.value.value})
		elif numeric_filter.clause is Clause.NOT_EQUAL:
			return ~Q(**{f"{numeric_filter.table_field}": numeric_filter.value.value})
		elif numeric_filter.clause is Clause.GREATER_THAN:
			return Q(**{f"{numeric_filter.table_field}__gt": numeric_filter.value.value})
		elif numeric_filter.clause is Clause.LESS_THAN:
			return Q(**{f"{numeric_filter.table_field}__lt": numeric_filter.value.value})
		elif numeric_filter.clause is Clause.GREATER_THAN_OR_EQUAL:
			return Q(**{f"{numeric_filter.table_field}__gte": numeric_filter.value.value})
		elif numeric_filter.clause is Clause.LESS_THAN_OR_EQUAL:
			return Q(**{f"{numeric_filter.table_field}__lte": numeric_filter.value.value})

		raise NotImplementedError(f"Unknown numeric filter clause: \"{numeric_filter.clause}\"")
