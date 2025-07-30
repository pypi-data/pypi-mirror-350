from __future__ import annotations

import abc
import typing
from asyncio import AbstractEventLoop
from logging import getLogger

from pandas import DataFrame
from pydantic import ConfigDict

from statql.common import Model, TableIdentifier, FrozenModel, IConnector, IAsyncConnector, IntegrationIdentifier
from .terms import Term
from .utils import Estimation

logger = getLogger(__name__)


class StatQLContext(FrozenModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    event_loop: AbstractEventLoop
    connectors: typing.Mapping[IntegrationIdentifier, IConnector | IAsyncConnector]


class Batch(Model, abc.ABC):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    data: DataFrame


class PopulationPipelineBatch(Batch):
    integration_id: IntegrationIdentifier
    table_id: TableIdentifier
    table_size: int
    original_batch_size: int


class AggregationPipelineBatch(Batch):
    population_estimated_size: Estimation


class IPlanNode[BatchT: Batch](abc.ABC):
    @abc.abstractmethod
    def get_output_terms(self) -> typing.Set[Term]:
        raise NotImplementedError

    @abc.abstractmethod
    def execute(self, *, ctx: StatQLContext) -> typing.Generator[BatchT, None, None]:
        raise NotImplementedError
