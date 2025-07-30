import typing

from statql.common import FrozenModel, SamplingConfig, IConnectorConfig, IIntegrationDetails


class PostgresConnectorConfig(IConnectorConfig):
    host: str
    port: int
    user: str
    password: str
    scan_chunk_size: int = 10_000
    sampling_config: SamplingConfig = SamplingConfig()


class PostgresIntegrationDetails(IIntegrationDetails):
    host: str
    port: int
    user: str
    password_secret_name: str


class PostgresTableIdentifier(FrozenModel):
    db_name: str
    schema_name: str
    table_name: str

    def __str__(self):
        return f"{self.db_name}:{self.schema_name}:{self.table_name}"


class PostgresTableInfo(FrozenModel):
    table_identifier: PostgresTableIdentifier
    column_names: typing.AbstractSet[str]
