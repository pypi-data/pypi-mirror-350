from __future__ import annotations

import typing
from logging import getLogger

from statql.common import timer
from .reservoir import Reservoir
from ..common import IPlanNode, StatQLContext, Term, Batch, PopulationPipelineBatch, validate_columns

logger = getLogger(__name__)


class UpdateReservoir(IPlanNode):
    def __init__(self, *, input: IPlanNode[PopulationPipelineBatch], reservoir: Reservoir):
        super().__init__()
        self._input = input
        self._reservoir = reservoir

    def get_output_terms(self) -> typing.Set[Term]:
        return self._input.get_output_terms()

    def execute(self, *, ctx: StatQLContext) -> typing.Generator[Batch, None, None]:
        for batch in self._input.execute(ctx=ctx):
            validate_columns(df=batch.data, expected_terms=self._input.get_output_terms())

            with timer(name="Update reservoir"):
                self._reservoir.ingest_population_pipeline_batch(batch=batch)

            yield batch  # Yielding just to comply with interface
