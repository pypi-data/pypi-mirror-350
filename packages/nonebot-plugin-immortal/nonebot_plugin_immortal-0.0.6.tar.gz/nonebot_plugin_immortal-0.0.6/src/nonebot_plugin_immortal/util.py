from nonebot.rule import is_type
from nonebot.adapters.onebot.v11 import GroupMessageEvent

from . import immortal_config


async def is_white(event: GroupMessageEvent) -> bool:
    return event.group_id in immortal_config.whitelist

is_basic = is_type(GroupMessageEvent) & is_white
