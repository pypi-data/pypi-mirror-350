from cascade_filter.filter import ChoiceFilter
from cascade_filter.clause import Clause

from django.db.models.query import Q


class ChoiceFilterMixin:
	def make_choice_filter(self, choice_filter: ChoiceFilter) -> Q:
		if choice_filter.clause is Clause.EQUAL:
			q = Q()

			for option in choice_filter.value.value:
				q |= Q(**{choice_filter.table_field: option})

			return q

		elif choice_filter.clause is Clause.NOT_EQUAL:
			q = Q()

			for option in choice_filter.value.value:
				q &= ~Q(**{choice_filter.table_field: option})

			return q

		raise NotImplementedError(f"Unknown choice filter clause: \"{choice_filter.clause}\"")
