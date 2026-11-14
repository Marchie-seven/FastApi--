
from fastapi import APIRouter,Depends,HTTPException,status,Query
import traceback
from config.db_conf import AsyncSession, get_db
from models.users import User
from schemas.favorite import FavoriteCheckRequest, FavoriteAddRequest
from utils.auth import get_current_user
from utils.response import success_response
from crud import favorite

router = APIRouter(prefix="/api/favorite",tags=["favorite"])

@router.get("/check")
async def check(new_id:int=Query(...,alias="newsId"),
                user:User=Depends(get_current_user),
                db:AsyncSession=Depends(get_db)
                ):
    is_favorite= await favorite.is_news_favorite(db,user_id=user.id,news_id=new_id)
    return success_response(message="检查收藏功能成功",data=FavoriteCheckRequest(isFavorite=is_favorite))

@router.post("/add")
async def add_favorite(
        data:FavoriteAddRequest,
        user:User=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
    result=await favorite.add_news_favorite(db,user.id,data.news_id)
    return success_response(message="添加收藏成功",data=result)













