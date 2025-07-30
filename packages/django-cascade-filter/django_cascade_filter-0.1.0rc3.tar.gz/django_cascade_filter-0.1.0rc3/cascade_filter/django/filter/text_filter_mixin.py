from cascade_filter.filter import TextFilter
from cascade_filter.clause import Clause

from django.db.models.query import Q


class TextFilterMixin:
	def make_text_filter(self, text_filter: TextFilter):
		if text_filter.clause is Clause.EQUAL:
			return Q(**{text_filter.table_field: text_filter.value.value})
		elif text_filter.clause is Clause.NOT_EQUAL:
			return ~Q(**{text_filter.table_field: text_filter.value.value})
		elif text_filter.clause is Clause.CONTAINS:
			return Q(**{f"{text_filter.table_field}__contains": text_filter.value.value})
		elif text_filter.clause is Clause.NOT_CONTAINS:
			return ~Q(**{f"{text_filter.table_field}__contains": text_filter.value.value})
		elif text_filter.clause is Clause.STARTS_WITH:
			return Q(**{f"{text_filter.table_field}__startswith": text_filter.value.value})
		elif text_filter.clause is Clause.ENDS_WITH:
			return Q(**{f"{text_filter.table_field}__endswith": text_filter.value.value})

		raise NotImplementedError(f"Unknown text filter clause: \"{text_filter.clause}\"")
