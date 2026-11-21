from fastapi import APIRouter, Depends, HTTPException, Query

from models.news import News
from utils.response import success_response
from config.db_conf import AsyncSession, get_db
from crud import history
from models.users import User
from schemas.history import HistoryAddResponse, HistoryAddRequest,HistoryListRequest
from utils.auth import get_current_user

router = APIRouter(prefix="/api/history", tags=["history"])
@router.post("/add")
async def add_history(
        data: HistoryAddRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    date=await history.add_history(data.news_id,user,db)
    res_data=HistoryAddResponse.model_validate(date)

    return success_response(message="添加历史记录成功",data=res_data)

@router.get("/list")
async def get_history_list(
        page: int = Query(1,ge=1),
        page_size: int = Query(10,ge=1,le=100),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    history_row,totals=await history.get_history(user,db,page,page_size)
    result=[{
        "history_id":history_id,
        "view_time":history_view,
        **news.__dict__
    } for news,history_view,history_id in history_row]
    has_more=totals>page*page_size
    res_data=HistoryListRequest(
        list=result,
        total=totals,
        has_more=has_more,
    )
    return success_response(message="获取历史记录成功",data=res_data)

@router.delete("/delete/{history_id}")
async def delete_history(
        history_id: int,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    await history.delete_history(history_id,user,db)
    return success_response(message="删除历史记录成功")

#清空浏览历史记录
@router.delete("/clear")
async def clear_history(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    await history.clear_history(user,db)
    return success_response(message="清空历史记录成功")





















