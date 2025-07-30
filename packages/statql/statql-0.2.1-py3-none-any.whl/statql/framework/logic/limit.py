import typing

from statql.common import timer
from ..common import IPlanNode, StatQLContext, Term, Batch, validate_columns


class Limit(IPlanNode):
    def __init__(self, *, input: IPlanNode, limit: int):
        super().__init__()
        self._input = input
        self._limit = limit

    def get_output_terms(self) -> typing.Set[Term]:
        return self._input.get_output_terms()

    def execute(self, *, ctx: StatQLContext) -> typing.Generator[Batch, None, None]:
        for batch in self._input.execute(ctx=ctx):
            validate_columns(df=batch.data, expected_terms=self._input.get_output_terms())

            with timer(name="Limit"):
                batch.data = batch.data[: self._limit]

            yield batch
