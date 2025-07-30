from cascade_filter.field_type import FieldType
from cascade_filter.filter.single import SingleFilter
from cascade_filter.filter.value import FilterValue


class DateFilterValue(FilterValue[str]):
	pass


class DateFilter(SingleFilter[str]):
	subtype = FieldType.DATE
