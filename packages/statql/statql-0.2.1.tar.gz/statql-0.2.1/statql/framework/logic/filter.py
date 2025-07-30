import typing

from statql.common import timer
from ..common import (
    IPlanNode,
    StatQLContext,
    Term,
    get_term_column_name,
    validate_columns,
    PopulationPipelineBatch,
)


class Filter(IPlanNode):
    def __init__(self, *, input: IPlanNode[PopulationPipelineBatch], condition: Term):
        super().__init__()
        self._input = input
        self._condition = condition

    def get_output_terms(self) -> typing.Set[Term]:
        return self._input.get_output_terms()

    def execute(self, *, ctx: StatQLContext) -> typing.Generator[PopulationPipelineBatch, None, None]:
        for batch in self._input.execute(ctx=ctx):
            validate_columns(df=batch.data, expected_terms=self._input.get_output_terms())

            with timer(name="Filtering"):
                condition_column_name = get_term_column_name(self._condition)
                filter_series = batch.data[condition_column_name].astype(bool)
                batch.data = batch.data[filter_series]

            yield batch
