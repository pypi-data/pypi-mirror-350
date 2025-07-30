from cascade_filter.field_type import FieldType
from cascade_filter.filter.single import SingleFilter
from cascade_filter.filter.value import FilterValue


class TextFilterValue(FilterValue[str]):
	pass


class TextFilter(SingleFilter[str]):
	subtype = FieldType.TEXT
