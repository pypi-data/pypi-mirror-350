from cascade_filter.meta.field.field import Field
from cascade_filter.field_type import FieldType
from cascade_filter.meta.choice import Choice

from typing import Iterable, Union, Callable


ChoicesIterable = Iterable[Choice]
ChoicesCallable = Callable[..., ChoicesIterable]
Choices = Union[ChoicesIterable, ChoicesCallable]


class ChoiceField(Field):
	type = FieldType.CHOICE
	choices: Choices

	def __init__(self, label: str, choices: Choices, nullable: bool = False) -> None:
		super().__init__(label, nullable)
		self.choices = choices

	def serialize(self) -> dict:
		serialized_data = super().serialize()

		if callable(self.choices):
			serialized_data["choices"] = [i.serialize() for i in self.choices()]
		else:
			serialized_data["choices"] = [i.serialize() for i in self.choices]

		return serialized_data
