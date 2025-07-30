from statql.common import PluginBlueprint
from .connector import PostgresConnector
from .definitions import PostgresIntegrationDetails
from .fe_controller import PostgresFEController

POSTGRES_BLUEPRINT = PluginBlueprint(
    catalog_name="pg",
    fe_controller_cls=PostgresFEController,
    connector_cls=PostgresConnector,
    integration_details_cls=PostgresIntegrationDetails,
)
