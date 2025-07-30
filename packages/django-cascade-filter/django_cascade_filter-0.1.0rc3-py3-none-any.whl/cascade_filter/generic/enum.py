from enum import Enum


class ExtendedEnum(Enum):
	@classmethod
	def has_value(cls, value) -> bool:
		return value in cls._value2member_map_
