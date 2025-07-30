from cascade_filter.field_type import FieldType
from cascade_filter.filter.single import SingleFilter
from cascade_filter.filter.value import FilterValue

from typing import List, Any


class ChoiceFilterValue(FilterValue[List[Any]]):
	pass


class ChoiceFilter(SingleFilter[List[Any]]):
	subtype = FieldType.CHOICE
