import typing

from pandas import DataFrame, Series

from statql.common import timer
from .scalar_functions import get_scalar_function_cls
from ..common import IPlanNode, StatQLContext, ScalarFunction, get_term_column_name, Constant, Term, Batch, validate_columns


class Project(IPlanNode):
    def __init__(self, *, input: IPlanNode, new_terms: typing.Set[ScalarFunction | Constant]):
        super().__init__()
        self._input = input
        self._new_terms = new_terms

    def get_output_terms(self) -> typing.Set[Term]:
        return self._new_terms | self._input.get_output_terms()

    def execute(self, *, ctx: StatQLContext) -> typing.Generator[Batch, None, None]:
        for batch in self._input.execute(ctx=ctx):
            validate_columns(df=batch.data, expected_terms=self._input.get_output_terms())

            with timer(name="Project"):
                for term in self._new_terms:
                    if isinstance(term, Constant):
                        batch.data[get_term_column_name(term)] = term.value
                    elif isinstance(term, ScalarFunction):
                        batch.data[get_term_column_name(term)] = self._calculate_scalar_function(df=batch.data, func=term)
                    else:
                        raise TypeError

            yield batch

    @classmethod
    def _calculate_scalar_function(cls, *, df: DataFrame, func: ScalarFunction) -> Series:
        column_arguments = []
        scalar_arguments = []

        for arg in func.arguments:
            arg_column_name = get_term_column_name(arg)

            column = df.get(arg_column_name)

            if column is not None:
                column_arguments.append(column)

            elif isinstance(arg, Constant):
                scalar_arguments.append(arg.value)

            elif isinstance(arg, ScalarFunction):
                column_arguments.append(cls._calculate_scalar_function(df=df, func=arg))

            else:
                raise TypeError(f"Unsupported argument type: {type(arg).__name__}")

        scalar_func_cls = get_scalar_function_cls(func_name=func.func_name)
        result = scalar_func_cls.execute(*column_arguments, *scalar_arguments)
        return result
