from cascade_filter.filter import BaseFilter, SingleFilter, MultiFilter
from cascade_filter.django.filter.multi_filter_mixin import MultiFilterMixin

from typing import TypeVar

from django.db.models.base import Model
from django.db.models.query import QuerySet


T = TypeVar("T", bound=Model)


class Filter(MultiFilterMixin):
	cascade_filter: BaseFilter

	def __init__(self, cascade_filter: BaseFilter) -> None:
		self.cascade_filter = cascade_filter

	def filter(self, qs: QuerySet[T]) -> QuerySet[T]:
		if isinstance(self.cascade_filter, SingleFilter):
			q = self.make_single_filter(self.cascade_filter)
		elif isinstance(self.cascade_filter, MultiFilter):
			q = self.make_multi_filter(self.cascade_filter)
		else:
			raise NotImplementedError(f"Unknown filter type: {type(self.cascade_filter)}")

		return qs.filter(q)
