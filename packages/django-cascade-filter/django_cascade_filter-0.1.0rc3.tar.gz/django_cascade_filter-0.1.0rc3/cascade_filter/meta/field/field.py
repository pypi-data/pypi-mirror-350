from cascade_filter.field_type import FieldType

from typing import ClassVar


class Field:
	type: ClassVar[FieldType]
	label: str
	nullable: bool

	def __init__(self, label: str, nullable: bool = False) -> None:
		self.label = label
		self.nullable = nullable

	def serialize(self) -> dict:
		return {
			"type": self.type.value,
			"label": self.label,
			"nullable": self.nullable,
		}
