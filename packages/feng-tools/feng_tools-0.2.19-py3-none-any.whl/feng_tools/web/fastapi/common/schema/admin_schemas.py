from pydantic import BaseModel


class AdminAppInfo(BaseModel):
    api_prefix:str