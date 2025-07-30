from cascade_filter.filter import BaseFilter

from abc import ABC, abstractmethod


class BaseChecker(ABC):
	cascade_filter: BaseFilter

	def __init__(self, cascade_filter: BaseFilter) -> None:
		self.cascade_filter = cascade_filter

	@abstractmethod
	def is_fit(self, obj: object) -> bool: ...
