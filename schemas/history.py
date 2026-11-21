from datetime import datetime
from pydantic import BaseModel, Field,ConfigDict

from schemas.base import NewsItemBase


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

class HistoryViewTime(NewsItemBase):
    model_config =ConfigDict(from_attributes=True,
                            populate_by_name=True,
                             )
    history_id: int=Field(alias='historyId')
    view_time: datetime=Field(alias='viewTime')
class HistoryListRequest(BaseModel):
    list:list[HistoryViewTime]
    total:int=Field(alias='total')
    has_more: bool=Field(alias='hasMore')
    model_config = ConfigDict(from_attributes=True,
                              populate_by_name=True)











