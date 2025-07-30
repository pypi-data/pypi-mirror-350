from cascade_filter.generic.enum import ExtendedEnum

from typing import Final, FrozenSet


class Clause(ExtendedEnum):
	EQUAL = "=="
	NOT_EQUAL = "!="
	GREATER_THAN = ">"
	LESS_THAN = "<"
	GREATER_THAN_OR_EQUAL = ">="
	LESS_THAN_OR_EQUAL = "<="
	CONTAINS = "contains"
	NOT_CONTAINS = "not contains"
	IS = "is"
	IS_NOT = "is not"
	STARTS_WITH = "starts with"
	ENDS_WITH = "ends with"
	AND = "and"
	OR = "or"



CLAUSES_STRICT_COMPARISON: Final[FrozenSet[Clause]] = frozenset((Clause.EQUAL, Clause.NOT_EQUAL))
CLAUSES_NON_STRICT_COMPARISON: Final[FrozenSet[Clause]] = frozenset((
	Clause.GREATER_THAN, Clause.LESS_THAN, Clause.GREATER_THAN_OR_EQUAL, Clause.LESS_THAN_OR_EQUAL,
))
CLAUSES_CONTAINING: Final[FrozenSet[Clause]] = frozenset((Clause.CONTAINS, Clause.NOT_CONTAINS))
CLAUSES_ACCORDANCE: Final[FrozenSet[Clause]] = frozenset((Clause.IS, Clause.IS_NOT))
CLAUSES_BOUNDARY: Final[FrozenSet[Clause]] = frozenset((Clause.STARTS_WITH, Clause.ENDS_WITH))
