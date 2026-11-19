from fastapi import APIRouter, Depends, HTTPException
from utils.response import success_response
from config.db_conf import AsyncSession, get_db
from crud import history
from models.users import User
from schemas.history import HistoryAddResponse, HistoryAddRequest
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

























