import abc
import typing

from pandas import Series

from ..common import ScalarFunctionNames


class IScalarFunction(abc.ABC):
    name: typing.ClassVar[ScalarFunctionNames]
    num_args: typing.ClassVar[int]

    def __init_subclass__(cls, **kwargs):
        _ = cls.num_args  # Validating existence
        SCALAR_FUNCTION_NAME_TO_CLS[cls.name] = cls
        super().__init_subclass__(**kwargs)

    @classmethod
    def execute(cls, *arguments: Series) -> Series:
        raise NotImplementedError


SCALAR_FUNCTION_NAME_TO_CLS: typing.Dict[ScalarFunctionNames, typing.Type[IScalarFunction]] = {}


def get_scalar_function_cls(*, func_name: ScalarFunctionNames) -> typing.Type[IScalarFunction]:
    return SCALAR_FUNCTION_NAME_TO_CLS[func_name]


class GetFileExt(IScalarFunction):
    name = ScalarFunctionNames.GET_FILE_EXT
    num_args = 1

    @classmethod
    def execute(cls, arg: Series) -> Series:
        return arg.str.extract(r"\.([^.\\/]+)$", expand=False)


class Concat(IScalarFunction):
    name = ScalarFunctionNames.CONCAT
    num_args = 2

    @classmethod
    def execute(cls, a: Series, b: Series | str) -> Series:
        return a + b


class Split(IScalarFunction):
    name = ScalarFunctionNames.SPLIT
    num_args = 2

    @classmethod
    def execute(cls, column: Series, split_by: str) -> Series:
        return column.str.split(split_by, regex=False)


class GetItem(IScalarFunction):
    name = ScalarFunctionNames.GET_ITEM
    num_args = 2

    @classmethod
    def execute(cls, column: Series, key: int | typing.Hashable) -> Series:
        return column.str[key]


class Add(IScalarFunction):
    name = ScalarFunctionNames.ADD
    num_args = 2

    @classmethod
    def execute(cls, a: Series | int | float, b: Series | int | float) -> Series:  # TODO: Inaccurate.. int+int->int
        return a + b


class Subtract(IScalarFunction):
    name = ScalarFunctionNames.SUB
    num_args = 2

    @classmethod
    def execute(cls, a: Series | int | float, b: Series | int | float) -> Series:  # TODO: Inaccurate.. int-int->int
        return a - b


class Multiply(IScalarFunction):
    name = ScalarFunctionNames.MUL
    num_args = 2

    @classmethod
    def execute(cls, a: Series | int | float, b: Series | int | float) -> Series:  # TODO: Inaccurate.. int*int->int
        return a * b


class Divide(IScalarFunction):
    name = ScalarFunctionNames.DIV
    num_args = 2

    @classmethod
    def execute(cls, a: Series | int | float, b: Series | int | float) -> Series:  # TODO: Inaccurate.. int/int->int
        return a / b


class Eq(IScalarFunction):
    name = ScalarFunctionNames.EQ
    num_args = 2

    @classmethod
    def execute(cls, a: Series | typing.Any, b: Series | typing.Any) -> Series:  # TODO: Inaccurate.. int==int->bool
        return a == b


class Neq(IScalarFunction):
    name = ScalarFunctionNames.NEQ
    num_args = 2

    @classmethod
    def execute(cls, a: Series | typing.Any, b: Series | typing.Any) -> Series:  # TODO: Inaccurate.. int!=int->bool
        return a != b


class Or(IScalarFunction):
    name = ScalarFunctionNames.OR
    num_args = 2

    @classmethod
    def execute(cls, a: Series | typing.Any, b: Series | typing.Any) -> Series:  # TODO: Inaccurate.. int or int->bool
        return (a.astype(bool) if isinstance(a, Series) else bool(a)) | (b.astype(bool) if isinstance(b, Series) else bool(b))


class And(IScalarFunction):
    name = ScalarFunctionNames.AND
    num_args = 2

    @classmethod
    def execute(cls, a: Series | typing.Any, b: Series | typing.Any) -> Series:  # TODO: Inaccurate.. int and int->bool
        return (a.astype(bool) if isinstance(a, Series) else bool(a)) & (b.astype(bool) if isinstance(b, Series) else bool(b))


class Gt(IScalarFunction):
    name = ScalarFunctionNames.GT
    num_args = 2

    @classmethod
    def execute(cls, a: Series | typing.Any, b: Series | typing.Any) -> Series:  # TODO: Inaccurate.. int>int->bool
        return a > b


class GTE(IScalarFunction):
    name = ScalarFunctionNames.GTE
    num_args = 2

    @classmethod
    def execute(cls, a: Series | typing.Any, b: Series | typing.Any) -> Series:  # TODO: Inaccurate.. int>=int->bool
        return a >= b


class LT(IScalarFunction):
    name = ScalarFunctionNames.LT
    num_args = 2

    @classmethod
    def execute(cls, a: Series | typing.Any, b: Series | typing.Any) -> Series:  # TODO: Inaccurate.. int<int->bool
        return a < b


class LT(IScalarFunction):
    name = ScalarFunctionNames.LTE
    num_args = 2

    @classmethod
    def execute(cls, a: Series | typing.Any, b: Series | typing.Any) -> Series:  # TODO: Inaccurate.. int<=int->bool
        return a <= b
