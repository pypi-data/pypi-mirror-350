from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config


__plugin_meta__ = PluginMetadata(
    name="Immortal",
    description="修仙插件",
    usage="修仙娱乐",
)

immortal_config = get_plugin_config(Config)
