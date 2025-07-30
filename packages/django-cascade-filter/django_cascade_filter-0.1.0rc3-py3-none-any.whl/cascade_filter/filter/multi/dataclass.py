from cascade_filter.clause import Clause
from cascade_filter.filter.base import BaseFilter
from cascade_filter.filter.type import FilterType

from typing import List


class MultiFilter(BaseFilter):
	__slots__ = BaseFilter.__slots__ + ("subfilters", )

	type = FilterType.MULTI
	subfilters: List[BaseFilter]

	def __init__(self, clause: Clause, enabled: bool, subfilters: List[BaseFilter]) -> None:
		super().__init__(clause, enabled)
		self.subfilters = subfilters
