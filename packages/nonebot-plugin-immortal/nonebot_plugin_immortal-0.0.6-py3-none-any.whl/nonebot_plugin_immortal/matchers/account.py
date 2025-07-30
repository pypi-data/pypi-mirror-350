from zlib import adler32

from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment

from nonebot_plugin_orm import get_session

from nonebot_plugin_immortal.storage import Account
from nonebot_plugin_immortal.util import is_basic


account_register = on_command(
    cmd="修仙注册",
    rule=is_basic,
)

@account_register.handle()
async def _(event: GroupMessageEvent):
    # TODO: We dont check if it exists
    account = Account(
        user_id=event.user_id,
        ident=hex(adler32(event.get_user_id().encode()))[2:].ljust(8, "0")  # TODO: We assume it to be unique
    )
    async with get_session() as db_session:
        db_session.add(account)
        await db_session.commit()
    await account_register.finish(Message([
        MessageSegment.reply(id_=event.message_id),
        MessageSegment.text(text="注册成功")
    ]))
