from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class NewsItemBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    category_id: Optional[int] = Field(None, serialization_alias="categoryId")
    views: Optional[int] = None
    publish_time: Optional[datetime] = Field(None, serialization_alias="publishTime")
    model_config=ConfigDict(from_attributes=True, populate_by_name=True)