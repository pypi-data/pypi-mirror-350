from cascade_filter.meta.field.choice_field import ChoiceField
from cascade_filter.field_type import FieldType


class ArrayField(ChoiceField):
	type = FieldType.ARRAY
