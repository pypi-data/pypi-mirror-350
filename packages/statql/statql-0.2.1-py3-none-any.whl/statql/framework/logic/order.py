import typing

from statql.common import timer
from ..common import IPlanNode, Term, StatQLContext, get_term_column_name, Batch, validate_columns


class Order(IPlanNode):
    def __init__(self, *, input: IPlanNode, term: Term, desc: bool = False):
        super().__init__()
        self._input = input
        self._term = term
        self._desc = desc

    def get_output_terms(self) -> typing.Set[Term]:
        return self._input.get_output_terms()

    def execute(self, *, ctx: StatQLContext) -> typing.Generator[Batch, None, None]:
        for batch in self._input.execute(ctx=ctx):
            validate_columns(df=batch.data, expected_terms=self._input.get_output_terms())

            with timer(name="Order"):
                batch.data.sort_values(by=get_term_column_name(self._term), ascending=not self._desc, inplace=True)

            yield batch
