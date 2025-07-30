from pulsekit.plugin.plugin import PluginBase, PluginType


class LocalPlugin(PluginBase):
    def get_type(self) ->PluginType:
        return PluginType.Builtin

