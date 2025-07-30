from cascade_filter.field_type import FieldType
from cascade_filter.filter.single import SingleFilter
from cascade_filter.filter.value import FilterValue


class NumericFilterValue(FilterValue[int]):
	pass


class NumericFilter(SingleFilter[int]):
	subtype = FieldType.NUMERIC
