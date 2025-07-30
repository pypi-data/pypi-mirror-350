from statql.common import PluginBlueprint
from .connector import FileSystemConnector
from .definitions import FileSystemIntegrationDetails
from .fe_controller import FileSystemFEController

FILE_SYSTEM_BLUEPRINT = PluginBlueprint(
    catalog_name="fs",
    fe_controller_cls=FileSystemFEController,
    connector_cls=FileSystemConnector,
    integration_details_cls=FileSystemIntegrationDetails,
)
