from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.news import Category
async def get_categories(db:AsyncSession,skip:int=0, limit:int=100,):
    stml=select(Category).offset(skip).limit(limit)
    result=await db.execute(stml)
    return result.scalars().all()







