from __future__ import annotations

import random
import typing
from dataclasses import dataclass
from threading import Lock

import numpy as np
from pandas import DataFrame, concat

from statql.common import StatQLInternalColumns, scale_sequence, IntegrationIdentifier, TableIdentifier
from ..common import Term, get_term_column_name, Estimation, PopulationPipelineBatch, AggregationPipelineBatch


class Reservoir:
    def __init__(self, *, table_reservoir_max_size: int, terms: typing.AbstractSet[Term]):
        self._lock = Lock()
        self._table_reservoir_max_size = table_reservoir_max_size
        self._tables: typing.Dict[typing.Tuple[IntegrationIdentifier, TableIdentifier], _TableInfo] = {}  # TODO: Make it configurable
        self._terms = terms

    def ingest_population_pipeline_batch(self, *, batch: PopulationPipelineBatch) -> None:
        with self._lock:
            if batch.original_batch_size == 0:
                return  # We don't care about empty batches

            table_key = (batch.integration_id, batch.table_id)
            table_info = self._tables.get(table_key)

            if table_info is None:
                table_info = _TableInfo(
                    table_size=batch.table_size,
                    data_reservoir=_TableDataReservoir(reservoir_max_size=self._table_reservoir_max_size),
                    population_ratios_reservoir=_TablePopulationRatiosReservoir(reservoir_max_size=self._table_reservoir_max_size),
                )
                self._tables[table_key] = table_info

            table_info.table_size = batch.table_size
            table_info.data_reservoir.ingest_data(data=batch.data)
            table_info.population_ratios_reservoir.ingest_population_ratio_observation(population_ratio=len(batch.data) / batch.original_batch_size)

    def build_aggregation_pipeline_batch(self) -> AggregationPipelineBatch:
        with self._lock:
            # Returns sample and estimated total size of all tables
            table_identifier_to_population_size_estimation = {}

            for table, table_info in list(self._tables.items()):
                # If table size estimation is smaller than reservoir size, then it is incorrect
                fixed_table_size = max(table_info.table_size, table_info.data_reservoir.reservoir_size)
                table_identifier_to_population_size_estimation[table] = table_info.population_ratios_reservoir.estimate_population_ratio() * fixed_table_size

            total_population_estimated_size = Estimation.sum_independent_ests(table_identifier_to_population_size_estimation.values())

            if total_population_estimated_size.value == 0:
                return AggregationPipelineBatch(
                    data=DataFrame(columns=[get_term_column_name(term) for term in self._terms]),
                    population_estimated_size=total_population_estimated_size,
                )

            samples: typing.List[DataFrame] = []

            for table, size_est in table_identifier_to_population_size_estimation.items():
                table_info = self._tables[table]
                table_size_ratio = size_est.value / total_population_estimated_size.value
                table_sample = table_info.data_reservoir.sample(sample_size=max(int(table_size_ratio * self._table_reservoir_max_size), 1))
                samples.append(table_sample)

            if samples:
                return AggregationPipelineBatch(
                    data=concat(samples, ignore_index=True),
                    population_estimated_size=total_population_estimated_size,
                )
            else:
                return AggregationPipelineBatch(
                    data=DataFrame(columns=[get_term_column_name(term) for term in self._terms]),
                    population_estimated_size=total_population_estimated_size,
                )

    @property
    def terms(self) -> typing.Set[Term]:
        return set(self._terms)


@dataclass
class _TableInfo:
    table_size: int
    data_reservoir: _TableDataReservoir
    population_ratios_reservoir: _TablePopulationRatiosReservoir


class _TableDataReservoir:
    def __init__(self, *, reservoir_max_size: int):
        self._reservoir_max_size = reservoir_max_size
        self._canonical_columns: typing.List[str] | None = None
        self._visited_row_count = 0
        self._row_ids_in_reservoir = set()
        self._table_data_reservoir: typing.List[typing.Tuple] = []

    def ingest_data(self, *, data: DataFrame) -> None:
        # We are sorting columns by name because we rely on consistent column order later on
        if not self._canonical_columns:
            self._canonical_columns = sorted(data.columns)

        data = data[self._canonical_columns]

        row_id_index = self._canonical_columns.index(StatQLInternalColumns.ROW_ID)

        for row in data.itertuples(index=False):
            self._visited_row_count += 1

            row_id = row[row_id_index]

            if row_id in self._row_ids_in_reservoir:
                continue

            if len(self._table_data_reservoir) < self._reservoir_max_size:
                self._table_data_reservoir.append(row)
                self._row_ids_in_reservoir.add(row_id)
            else:
                index = random.randint(0, self._visited_row_count)

                if index < self._reservoir_max_size:
                    reservoir_row_id_to_replace = self._table_data_reservoir[index][row_id_index]
                    self._row_ids_in_reservoir.remove(reservoir_row_id_to_replace)
                    self._row_ids_in_reservoir.add(row_id)
                    self._table_data_reservoir[index] = row

    def sample(self, *, sample_size: int) -> DataFrame:
        if sample_size < 1:
            raise ValueError

        # If the reservoir is smaller than its max size, we scale it artificially by replicating elements.
        if len(self._table_data_reservoir) < self._reservoir_max_size:
            scale_factor = self._reservoir_max_size / len(self._table_data_reservoir)
            reservoir = scale_sequence(seq=self._table_data_reservoir, factor=scale_factor)
        else:
            reservoir = self._table_data_reservoir

        sample = random.sample(reservoir, sample_size)

        df = DataFrame(sample)
        df.columns = self._canonical_columns
        df.drop(StatQLInternalColumns.ROW_ID, axis=1, inplace=True)

        return df

    @property
    def reservoir_size(self) -> int:
        return len(self._table_data_reservoir)


class _TablePopulationRatiosReservoir:
    """
    Sometimes we get a batch from `Scan` node with size 1000, and then it is narrowed down to 700 due to filtering.
    The next batch is of size 1100 is narrowed down to 650, etc...
    This means that `relevant population`/`entire population` ratio is a random variable.
    We want to estimate the value of this random variable because it is used for scaling aggregation values (like SUM or COUNT).
    In order to get a good estimate, we use reservoir sampling which is implemented in this class.
    """

    def __init__(self, *, reservoir_max_size: int):
        self._reservoir_max_size = reservoir_max_size
        self._ratios_count = 0
        self._population_ratios_reservoir: typing.List[float] = []

    def ingest_population_ratio_observation(self, *, population_ratio: float) -> None:
        self._ratios_count += 1

        if self._ratios_count < self._reservoir_max_size:
            self._population_ratios_reservoir.append(population_ratio)
        else:
            index = random.randint(0, self._ratios_count)

            if index < self._reservoir_max_size:
                self._population_ratios_reservoir[index] = population_ratio

    def estimate_population_ratio(self, *, alpha: float = 0.05, bootstrap_iterations: int = 1000) -> Estimation:
        data = np.array(self._population_ratios_reservoir)
        n = data.shape[0]

        samples = np.random.choice(data, size=(bootstrap_iterations, n), replace=True)

        means = samples.mean(axis=1)

        lower, upper = np.percentile(means, [100 * (alpha / 2), 100 * (1 - alpha / 2)])

        point_estimation = data.mean()

        return Estimation(point_estimation, (upper - lower) / 2)
