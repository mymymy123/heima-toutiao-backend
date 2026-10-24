from pydantic import BaseModel,Field,ConfigDict
from schemas.base import NewsItemBase
from datetime import datetime


class HistoryAddRequest(BaseModel):
    news_id:int=Field(...,alias='newsId')



class HistoryListNewsItem(NewsItemBase):
    history_id:int=Field(alias='historyId')
    view_time:datetime=Field(alias='viewTime')

    model_config=ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )


class HistoryListResponse(BaseModel):
    list:list[HistoryListNewsItem]
    total:int
    has_more:bool=Field(alias='hasMore')

    model_config=ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )