from nonebot.plugin import PluginMetadata, require

require("nonebot_plugin_alconna")
require("nonebot_plugin_orm")

from nonebot import get_plugin_config

from .config import Config
from . import matchers as matchers


__plugin_meta__ = PluginMetadata(
    name="Immortal",
    description="修仙插件",
    usage="修仙娱乐",

    type="application",
    homepage="https://github.com/BrokenC1oud/nonebot-plugin-immortal",

)

immortal_config = get_plugin_config(Config)
