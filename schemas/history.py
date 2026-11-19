from datetime import datetime
from pydantic import BaseModel, Field,ConfigDict


class HistoryAddRequest(BaseModel):
    news_id: int=Field(alias='newsId')

class HistoryAddResponse(BaseModel):
    model_config =ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )
    id : int=Field(alias='id')
    user_id : int=Field(alias='userId')
    news_id : int=Field(alias='newsId')
    view_time : datetime=Field(alias='viewTime')













