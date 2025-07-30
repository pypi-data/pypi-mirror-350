from cascade_filter.filter import SingleFilter
from cascade_filter.compliance_checker.base import BaseChecker

from typing import TypeVar, Generic


T = TypeVar("T", bound=SingleFilter)


class SingleChecker(BaseChecker, Generic[T]):
	cascade_filter: T

	def __init__(self, cascade_filter: T) -> None:
		super().__init__(cascade_filter)
