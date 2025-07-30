from __future__ import annotations

import abc
import enum
import typing

from statql.common import FrozenModel


class ScalarFunctionNames(enum.StrEnum):
    GET_FILE_EXT = "get_file_ext"
    CONCAT = "concat"
    SPLIT = "split"
    GET_ITEM = "get_item"

    # Math operators
    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    DIV = "div"

    # Bool operators
    EQ = "eq"
    NEQ = "neq"
    OR = "or"
    AND = "and"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"


class AggregationFunctionNames(enum.StrEnum):
    AVG = "AVG"
    SUM = "SUM"
    COUNT = "COUNT"


class Term(FrozenModel, abc.ABC):
    @abc.abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_args(self) -> typing.List[Term]:
        raise NotImplementedError

    def get_args_recursive(self) -> typing.Set[Term]:
        args = set()

        for arg in self.get_args():
            args.add(arg)
            args.update(arg.get_args())

        return args


class TableColumn(Term):
    column_name: str

    def get_name(self) -> str:
        return self.column_name

    def get_args(self) -> typing.List[Term]:
        return []


class Constant(Term):
    value: typing.Any

    def get_name(self) -> str:
        return str(self.value)

    def get_args(self) -> typing.List[Term]:
        return []


class ScalarFunction(Term):
    func_name: ScalarFunctionNames
    arguments: typing.Tuple[Term, ...]

    def get_name(self) -> str:
        arguments = ", ".join(arg.get_name() for arg in self.arguments)
        return f"{self.func_name}({arguments})"

    def get_args(self) -> typing.List[Term]:
        return list(self.arguments)


class AggregationFunction(Term):
    func_name: AggregationFunctionNames
    argument: Term | None

    def get_name(self) -> str:
        return f"{self.func_name}({self.argument.get_name()})" if self.argument else f"{self.func_name}()"

    def get_args(self) -> typing.List[Term]:
        return [self.argument] if self.argument else []
