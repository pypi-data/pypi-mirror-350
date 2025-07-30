from pydantic import BaseModel


class Config(BaseModel):
    """ 插件配置 """
    db_provider: str

    whitelist: list[int] = []
