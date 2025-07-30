from cascade_filter.field_type import FieldType
from cascade_filter.filter.single import SingleFilter
from cascade_filter.filter.value import FilterValue


class BooleanFilterValue(FilterValue[bool]):
	pass


class BooleanFilter(SingleFilter[bool]):
	subtype = FieldType.BOOLEAN
