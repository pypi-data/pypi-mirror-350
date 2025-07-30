from cascade_filter.filter import DateFilter
from cascade_filter.clause import Clause

from django.db.models.query import Q


class DateFilterMixin:
	def make_date_filter(self, date_filter: DateFilter) -> Q:
		if date_filter.clause is Clause.EQUAL:
			return Q(**{date_filter.table_field: date_filter.value.value})
		elif date_filter.clause is Clause.NOT_EQUAL:
			return ~Q(**{f"{date_filter.table_field}": date_filter.value.value})
		elif date_filter.clause is Clause.GREATER_THAN:
			return Q(**{f"{date_filter.table_field}__gt": date_filter.value.value})
		elif date_filter.clause is Clause.LESS_THAN:
			return Q(**{f"{date_filter.table_field}__lt": date_filter.value.value})
		elif date_filter.clause is Clause.GREATER_THAN_OR_EQUAL:
			return Q(**{f"{date_filter.table_field}__gte": date_filter.value.value})
		elif date_filter.clause is Clause.LESS_THAN_OR_EQUAL:
			return Q(**{f"{date_filter.table_field}__lte": date_filter.value.value})

		raise NotImplementedError(f"Unknown date filter clause: \"{date_filter.clause}\"")
