import datetime

from nonebot_plugin_orm import Model

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class Account(Model):
    __table_name__ = "nonebot_plugin_immortal_account"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    ident: Mapped[str] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    cultivation: Mapped[int] = mapped_column(default=0)  # 修为
    spirit_stone: Mapped[int] = mapped_column(default=0)
