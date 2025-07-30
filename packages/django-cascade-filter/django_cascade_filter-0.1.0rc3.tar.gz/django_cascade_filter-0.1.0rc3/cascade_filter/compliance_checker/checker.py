from cascade_filter.filter import (
	BaseFilter, SingleFilter, MultiFilter, DateFilter, ChoiceFilter, TextFilter, NumericFilter, BooleanFilter,
	ArrayFilter,
)
from cascade_filter.compliance_checker.base import BaseChecker
from cascade_filter.compliance_checker.single import SingleChecker
from cascade_filter.compliance_checker.multi import MultiChecker
from cascade_filter.compliance_checker.date import DateChecker
from cascade_filter.compliance_checker.choice import ChoiceChecker
from cascade_filter.compliance_checker.text import TextChecker
from cascade_filter.compliance_checker.numeric import NumericChecker
from cascade_filter.compliance_checker.boolean import BooleanChecker
from cascade_filter.compliance_checker.array import ArrayChecker


class ComplianceChecker:
	"""
	Allows to check the compliance of objects with the rules of cascade filters.
	"""
	checker: BaseChecker

	def __init__(self, cascade_filter: BaseFilter) -> None:
		if isinstance(cascade_filter, SingleFilter):
			self.checker = self.make_single_checker(cascade_filter)
		elif isinstance(cascade_filter, MultiFilter):
			self.checker = self.make_multi_checker(cascade_filter)
		else:
			raise NotImplementedError(f"Unknown filter type: {type(cascade_filter)}")

	def is_fit(self, obj: object) -> bool:
		if not self.checker.cascade_filter.enabled:
			return True

		return self.checker.is_fit(obj)

	@classmethod
	def make_single_checker(cls, cascade_filter: SingleFilter) -> SingleChecker:
		if isinstance(cascade_filter, DateFilter):
			return DateChecker(cascade_filter)
		elif isinstance(cascade_filter, ChoiceFilter):
			return ChoiceChecker(cascade_filter)
		elif isinstance(cascade_filter, TextFilter):
			return TextChecker(cascade_filter)
		elif isinstance(cascade_filter, NumericFilter):
			return NumericChecker(cascade_filter)
		elif isinstance(cascade_filter, BooleanFilter):
			return BooleanChecker(cascade_filter)
		elif isinstance(cascade_filter, ArrayFilter):
			return ArrayChecker(cascade_filter)

		raise NotImplementedError(f"Unknown filter type: {type(cascade_filter)}")

	@classmethod
	def make_multi_checker(cls, cascade_filter: MultiFilter) -> MultiChecker:
		subcheckers = []

		for subfilter in cascade_filter.subfilters:
			if not subfilter.enabled:
				continue

			if isinstance(subfilter, SingleFilter):
				subcheckers.append(cls.make_single_checker(subfilter))
			elif isinstance(subfilter, MultiFilter):
				subcheckers.append(cls.make_multi_checker(subfilter))
			else:
				raise NotImplementedError(f"Unknown filter type: {type(cascade_filter)}")

		return MultiChecker(cascade_filter, subcheckers)
