from cascade_filter.filter import BaseFilter
from cascade_filter.filter.value import FilterValue
from cascade_filter.clause import Clause
from cascade_filter.meta.field import FieldType
from cascade_filter.filter.type import FilterType

from abc import ABCMeta
from typing import ClassVar, TypeVar, Any, Generic


T = TypeVar("T", bound=Any)


class SingleFilter(BaseFilter, Generic[T], metaclass=ABCMeta):
	__slots__ = BaseFilter.__slots__ + ("table_field", "value")

	type = FilterType.SINGLE
	subtype: ClassVar[FieldType]
	table_field: str
	value: FilterValue[T]

	def __init__(self, clause: Clause, enabled: bool, table_field: str, value: FilterValue[T]):
		super().__init__(clause, enabled)
		self.table_field = table_field
		self.value = value
