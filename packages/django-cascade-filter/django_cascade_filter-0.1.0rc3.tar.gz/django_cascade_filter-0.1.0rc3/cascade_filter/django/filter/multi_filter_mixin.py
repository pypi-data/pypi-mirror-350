from cascade_filter.filter import MultiFilter, SingleFilter
from cascade_filter.clause import Clause
from cascade_filter.django.filter.single_filter_mixin import SingleFilterMixin

from django.db.models.query import Q


class MultiFilterMixin(SingleFilterMixin):
	def make_multi_filter(self, multi_filter: MultiFilter) -> Q:
		if not multi_filter.enabled:
			return Q()

		q = Q()

		for subfilter in multi_filter.subfilters:
			if isinstance(subfilter, SingleFilter):
				sub_q = self.make_single_filter(subfilter)
			elif isinstance(subfilter, MultiFilter):
				sub_q = self.make_multi_filter(subfilter)
			else:
				raise NotImplementedError(f"Unknown filter type: {type(subfilter)}")

			if multi_filter.clause is Clause.AND:
				q &= sub_q
			elif multi_filter.clause is Clause.OR:
				q |= sub_q
			else:
				raise NotImplementedError(f"Unknown multi-filter clause: \"{multi_filter.clause}\"")

		return q
