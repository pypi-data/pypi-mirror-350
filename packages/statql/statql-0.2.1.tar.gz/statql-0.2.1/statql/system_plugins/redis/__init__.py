from statql.common import PluginBlueprint
from .connector import RedisConnector
from .definitions import RedisIntegrationDetails
from .fe_controller import RedisFEController

REDIS_BLUEPRINT = PluginBlueprint(
    catalog_name="redis",
    fe_controller_cls=RedisFEController,
    connector_cls=RedisConnector,
    integration_details_cls=RedisIntegrationDetails,
)
