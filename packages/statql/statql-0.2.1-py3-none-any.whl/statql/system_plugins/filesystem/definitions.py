from statql.common import IIntegrationDetails, IConnectorConfig


class FileSystemConnectorConfig(IConnectorConfig):
    root_path: str
    scan_chunk_size: int = 10_000


class FileSystemIntegrationDetails(IIntegrationDetails):
    root_path: str
