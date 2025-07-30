from cascade_filter.clause import Clause
from cascade_filter.filter import MultiFilter
from cascade_filter.compliance_checker.base import BaseChecker

from typing import List


class MultiChecker(BaseChecker):
	cascade_filter: MultiFilter

	def __init__(self, cascade_filter: MultiFilter, subcheckers: List[BaseChecker]) -> None:
		super().__init__(cascade_filter)
		self.subcheckers = subcheckers

	def is_fit(self, obj: object) -> bool:
		if self.cascade_filter.clause is Clause.AND:
			return all((i.is_fit(obj) for i in self.subcheckers))
		elif self.cascade_filter.clause is Clause.OR:
			return any((i.is_fit(obj) for i in self.subcheckers))

		raise NotImplementedError(f"Unknown multi filter clause: {self.cascade_filter.clause}")
