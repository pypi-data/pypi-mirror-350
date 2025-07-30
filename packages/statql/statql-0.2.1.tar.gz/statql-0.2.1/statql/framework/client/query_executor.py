import time
import typing
from logging import getLogger
from threading import Thread

from pydantic import ConfigDict

from statql.common import Model
from .query_planner import ExecutionPlan
from ..common import StatQLContext, AggregationPipelineBatch, PopulationPipelineBatch, IPlanNode

logger = getLogger(__name__)


class PipelinesSharedState(Model):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    population_completed: bool = False
    population_pipeline_error: Exception | None = None

    aggregation_completed: bool = False


class QueryExecutor:
    @classmethod
    def execute(cls, *, plan: ExecutionPlan, ctx: StatQLContext) -> typing.Generator[AggregationPipelineBatch, None, None]:
        shared_state = PipelinesSharedState()

        population_thread = Thread(target=lambda: cls._run_population_pipeline(plan=plan.population_plan, ctx=ctx, shared_state=shared_state))
        population_thread.start()

        try:
            yield from cls._run_aggregation_pipeline(plan=plan.aggregation_plan, ctx=ctx, shared_state=shared_state)
        finally:
            population_thread.join()

        if shared_state.population_pipeline_error:
            raise shared_state.population_pipeline_error

    @classmethod
    def _run_population_pipeline(cls, *, plan: IPlanNode[PopulationPipelineBatch], ctx: StatQLContext, shared_state: PipelinesSharedState) -> None:
        try:
            for _ in plan.execute(ctx=ctx):
                if shared_state.aggregation_completed:
                    break

        except Exception as e:
            shared_state.population_pipeline_error = e

        finally:
            shared_state.population_completed = True

    @classmethod
    def _run_aggregation_pipeline(
        cls, *, plan: IPlanNode[AggregationPipelineBatch], ctx: StatQLContext, shared_state: PipelinesSharedState
    ) -> typing.Generator[AggregationPipelineBatch, None, None]:
        should_exit = False

        try:
            for output in plan.execute(ctx=ctx):
                yield output

                if should_exit:
                    break

                if shared_state.population_completed:
                    should_exit = True  # Yield one more and then exit
                    continue

                time.sleep(0.1)  # To not starve CPU

        finally:
            shared_state.aggregation_completed = True
