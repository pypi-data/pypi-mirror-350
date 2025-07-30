import typing

from statql.common import PluginBlueprint
from statql.system_plugins import SYSTEM_PLUGINS


class PluginsManager:
    _PLUGINS: typing.List[PluginBlueprint] = list(SYSTEM_PLUGINS)

    @classmethod
    def register(cls, *, plugin: PluginBlueprint) -> None:
        cls._PLUGINS.append(plugin)

    @classmethod
    def get_plugin_by_catalog_name(cls, *, catalog_name: str) -> PluginBlueprint:
        matching_plugins = [plugin for plugin in cls._PLUGINS if plugin.catalog_name == catalog_name]

        if not matching_plugins:
            raise LookupError(f"Plugin not found: {catalog_name}")

        if len(matching_plugins) > 1:
            raise RuntimeError(f"Found more than one plugin")

        return matching_plugins[0]

    @classmethod
    def get_all(cls) -> typing.List[PluginBlueprint]:
        return list(cls._PLUGINS)
