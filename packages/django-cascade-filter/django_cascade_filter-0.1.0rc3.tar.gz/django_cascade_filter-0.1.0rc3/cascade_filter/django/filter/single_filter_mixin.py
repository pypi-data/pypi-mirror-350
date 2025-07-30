from cascade_filter.django.filter.text_filter_mixin import TextFilterMixin
from cascade_filter.django.filter.date_filter_mixin import DateFilterMixin
from cascade_filter.django.filter.choice_filter_mixin import ChoiceFilterMixin
from cascade_filter.django.filter.numeric_filter_mixin import NumericFilterMixin
from cascade_filter.django.filter.boolean_filter_mixin import BooleanFilterMixin
from cascade_filter.django.filter.array_filter_mixin import ArrayFilterMixin
from cascade_filter.filter import (
	SingleFilter, DateFilter, ChoiceFilter, TextFilter, NumericFilter, BooleanFilter, ArrayFilter,
)

from django.db.models.query import Q


class SingleFilterMixin(
	TextFilterMixin, DateFilterMixin, ChoiceFilterMixin, NumericFilterMixin, BooleanFilterMixin, ArrayFilterMixin,
):
	def make_single_filter(self, single_filter: SingleFilter) -> Q:
		if not single_filter.enabled:
			return Q()

		if isinstance(single_filter, DateFilter):
			return self.make_date_filter(single_filter)
		elif isinstance(single_filter, ChoiceFilter):
			return self.make_choice_filter(single_filter)
		elif isinstance(single_filter, TextFilter):
			return self.make_text_filter(single_filter)
		elif isinstance(single_filter, NumericFilter):
			return self.make_numeric_filter(single_filter)
		elif isinstance(single_filter, BooleanFilter):
			return self.make_boolean_filter(single_filter)
		elif isinstance(single_filter, ArrayFilter):
			return self.make_array_filter(single_filter)

		raise NotImplementedError(f"Unknown filter subtype: \"{single_filter.subtype}\"")
