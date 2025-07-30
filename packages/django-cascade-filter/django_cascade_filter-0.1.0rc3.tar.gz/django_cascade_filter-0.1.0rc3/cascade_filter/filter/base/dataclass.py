from cascade_filter.filter.type import FilterType
from cascade_filter.clause import Clause

from abc import ABC
from typing import ClassVar


class BaseFilter(ABC):
	__slots__ = "clause", "enabled"

	type: ClassVar[FilterType]
	clause: Clause
	enabled: bool

	def __init__(self, clause: Clause, enabled: bool) -> None:
		self.clause = clause
		self.enabled = enabled
