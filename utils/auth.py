from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Header, Depends, HTTPException
from crud import users
from config.db_conf import get_db


# 整合根据Token查询用户，返回用户
async def get_current_user(authorization: str=Header(...,alias="Authorization")
                           ,db: AsyncSession=Depends(get_db)):
    token=authorization.split(" ")[1]
    user=await users.get_user_by_token(db,token)
    if not user:
        raise HTTPException(status_code=401,detail="无效的令牌或过期的令牌")
    return user























