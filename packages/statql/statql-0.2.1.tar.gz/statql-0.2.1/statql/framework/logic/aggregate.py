import math
from functools import partial
from logging import getLogger
from string import Template
from typing import Tuple, Generator, Any, Set, AbstractSet

import duckdb

from statql.common import FrozenModel
from ..common import (
    IPlanNode,
    StatQLContext,
    Term,
    AggregationFunction,
    get_term_column_name,
    Batch,
    AggregationPipelineBatch,
    validate_columns,
    AggregationFunctionNames,
    Estimation,
)

_GroupKey = Tuple[Any]


class _AggFuncDefinition(FrozenModel):
    duckdb_func: str
    requires_scaling: bool


def _build_agg_func_definitions():
    agg_func_definitions = {
        AggregationFunctionNames.AVG: _AggFuncDefinition(duckdb_func="AVG", requires_scaling=False),
        AggregationFunctionNames.SUM: _AggFuncDefinition(duckdb_func="SUM", requires_scaling=True),
        AggregationFunctionNames.COUNT: _AggFuncDefinition(duckdb_func="COUNT", requires_scaling=True),
    }

    if undefined_func_names := set(AggregationFunctionNames) - set(agg_func_definitions):
        raise RuntimeError(f"Some aggregation function names are missing definitions: {undefined_func_names}")

    return agg_func_definitions


_AGG_FUNC_DEFINITIONS = _build_agg_func_definitions()

logger = getLogger(__name__)


class Aggregate(IPlanNode):
    def __init__(
        self,
        *,
        input: IPlanNode[AggregationPipelineBatch],
        group_bys: AbstractSet[Term],
        aggregations: AbstractSet[AggregationFunction],
    ):
        super().__init__()
        self._input = input
        self._group_bys = group_bys
        self._aggregations = aggregations

    def get_output_terms(self) -> Set[Term]:
        return set(self._group_bys | self._aggregations)

    def execute(self, *, ctx: StatQLContext) -> Generator[Batch, None, None]:
        sql_template = self._build_query()

        for batch in self._input.execute(ctx=ctx):
            validate_columns(df=batch.data, expected_terms=self._input.get_output_terms())

            df = batch.data

            if len(df.columns) == 0:
                df["__statql_agg_dummy_column__"] = 73  # Adding dummy column in case there are no columns in the input batch, because duckdb expects 1 column

            sql = sql_template.substitute(
                df_var_name="df",
                df_length=len(batch.data),
                sample_size=len(batch.data),
                samples_count=100,
                scaling_factor=batch.population_estimated_size / max(len(batch.data), 1),
            )

            try:
                result = duckdb.execute(sql).fetchdf()
            except Exception as e:
                logger.exception(f"Failed to execute duckdb query - {e}:\n{sql}")
                raise

            # TODO: Can the next sections be optimized?

            # Formatting columns
            for column in result.columns:
                if column.startswith("final_"):
                    result[column[6:]] = result[column].apply(lambda item: Estimation(item[0], item[1]))
                    result.drop(columns=[column], inplace=True)

            # Scaling
            for agg_term in self._aggregations:
                if not _AGG_FUNC_DEFINITIONS[agg_term.func_name].requires_scaling:
                    continue

                column_name = get_term_column_name(agg_term)

                result[column_name] = result[column_name].apply(
                    partial(
                        self._scale_estimation,
                        sample_size=len(batch.data),
                        population_size=batch.population_estimated_size,
                    ),
                )

            batch.data = result

            yield batch

    @classmethod
    def _scale_estimation(cls, est: Estimation, *, sample_size: int, population_size: Estimation) -> Estimation:
        if sample_size == 0:
            return est

        # TODO: document this

        return Estimation(
            est.value * population_size.value / sample_size,
            math.hypot(
                est.value / sample_size * population_size.error,
                population_size.value / sample_size * est.error,
            ),
        )

    def _build_query(self) -> Template:
        estimates_cte_selects = ["rep_id"]
        estimates_cte_group_bys = ["rep_id"]
        final_selects = []
        final_group_bys = []

        for group_by in self._group_bys:
            estimates_cte_selects.append(f'"{get_term_column_name(group_by)}"')
            estimates_cte_group_bys.append(f'"{get_term_column_name(group_by)}"')
            final_selects.append(f'"{get_term_column_name(group_by)}"')
            final_group_bys.append(f'"{get_term_column_name(group_by)}"')

        for agg_term in self._aggregations:
            func_def = _AGG_FUNC_DEFINITIONS[agg_term.func_name]

            if agg_term.argument:
                agg = f'{func_def.duckdb_func}("{get_term_column_name(agg_term.argument)}")'
            else:
                agg = f"{func_def.duckdb_func}()"

            estimates_cte_selects.append(f'{agg} AS "{get_term_column_name(agg_term)}"')

            final_selects.append(
                f"""
                [
                    AVG("{get_term_column_name(agg_term)}"),
                    (quantile_cont("{get_term_column_name(agg_term)}", 0.975) - quantile_cont("{get_term_column_name(agg_term)}", 0.025)) / 2
                ] AS "final_{get_term_column_name(agg_term)}"
                """
            )

        return Template(
            # Setting that pandas_analyze_sample config to be larger than sample size
            # This is the amount of samples duckdb collects from the queried dataframe in order to determine column types
            # If we use something that is smaller than dataframe size, we might determine wrong duckdb column type
            f"""
            SET GLOBAL pandas_analyze_sample=9999999;
            WITH base AS (
                SELECT row_number() OVER () AS row_id, *
                FROM $df_var_name 
            ),
            draws AS (
                SELECT 
                    rep_id,
                    1 + floor(random() * $df_length) AS row_id
                FROM range($samples_count) AS r(rep_id), range($sample_size)
            ),
            estimates AS (
                SELECT
                    {", ".join(estimates_cte_selects)}
                FROM draws
                JOIN base USING (row_id)
                GROUP BY {", ".join(estimates_cte_group_bys)}
            )
            SELECT
                {", ".join(final_selects)}
            FROM estimates
            {("GROUP BY" + ", ".join(final_group_bys)) if final_group_bys else ""};
            """
        )
