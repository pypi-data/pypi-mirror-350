from cascade_filter.filter import BooleanFilter
from cascade_filter.clause import Clause

from django.db.models.query import Q


class BooleanFilterMixin:
	def make_boolean_filter(self, boolean_filter: BooleanFilter) -> Q:
		if boolean_filter.clause is Clause.IS:
			return Q(**{boolean_filter.table_field: boolean_filter.value.value})
		elif boolean_filter.clause is Clause.IS_NOT:
			return Q(**{boolean_filter.table_field: not boolean_filter.value.value})

		raise NotImplementedError(f"Unknown boolean filter clause: \"{boolean_filter.clause}\"")
