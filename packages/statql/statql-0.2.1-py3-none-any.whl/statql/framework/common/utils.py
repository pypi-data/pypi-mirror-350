import math
import typing
from functools import total_ordering

from pandas import DataFrame

from .terms import Term


def get_term_column_name(term: Term) -> str:
    return str(hash(term))


def validate_columns(*, df: DataFrame, expected_terms: typing.AbstractSet[Term]) -> None:
    for term in expected_terms:
        column_name = get_term_column_name(term)
        if column_name not in df.columns:
            raise ValueError(f"Term {repr(term)} not found in DataFrame (column name: {column_name})")


@total_ordering
class Estimation:
    def __init__(self, value: float, error: float):
        self.value = value
        self.error = error

    def __repr__(self):
        return f"{self.value:.2f}±{self.error:.2f}"

    # Addition and subtraction
    def __add__(self, other):
        if isinstance(other, Estimation):
            raise NotImplementedError

        return Estimation(self.value + other, self.error)

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, Estimation):
            raise NotImplementedError

        return Estimation(self.value - other, self.error)

    def __rsub__(self, other):
        if isinstance(other, Estimation):
            raise NotImplementedError

        return Estimation(other - self.value, self.error)

    # Multiplication
    def __mul__(self, other):
        if isinstance(other, Estimation):
            raise NotImplementedError

        return Estimation(self.value * other, abs(self.error * other))

    __rmul__ = __mul__

    # True‐division
    def __truediv__(self, other):
        if isinstance(other, Estimation):
            raise NotImplementedError

        return Estimation(self.value / other, abs(self.error / other))

    # Comparison
    def __eq__(self, other):
        if isinstance(other, Estimation):
            return self.value == other.value
        return self.value == other

    def __lt__(self, other):
        if isinstance(other, Estimation):
            return self.value < other.value
        return self.value < other

    def add_independent_est(self, other: typing.Self) -> None:
        self.value += other.value
        self.error = math.hypot(self.error, +other.error)

    @classmethod
    def sum_independent_ests(cls, ests: typing.Iterable[typing.Self]) -> typing.Self:
        total = cls(0, 0)
        for est in ests:
            total.add_independent_est(est)
        return total
