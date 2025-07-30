from cascade_filter.filter import ArrayFilter
from cascade_filter.clause import Clause

from django.db.models.query import Q


class ArrayFilterMixin:
	def make_array_filter(self, array_filter: ArrayFilter) -> Q:
		if array_filter.clause is Clause.CONTAINS:
			return Q(**{f"{array_filter.table_field}__contains": array_filter.value.value})
		elif array_filter.clause is Clause.NOT_CONTAINS:
			return ~Q(**{f"{array_filter.table_field}__contains": array_filter.value.value})

		raise NotImplementedError(f"Unknown array filter clause: \"{array_filter.clause}\"")
