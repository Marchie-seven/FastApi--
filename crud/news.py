from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.news import Category, News


async def get_categories(db:AsyncSession,skip:int=0, limit:int=100,):
    stml=select(Category).offset(skip).limit(limit)
    result=await db.execute(stml)
    return result.scalars().all()
async def get_news_list(db:AsyncSession,category_id:int,skip:int=0,limit:int=10):
    #查询指定分类下的所有新闻
    stmt=select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result=await db.execute(stmt)
    return result.scalars().all()
async  def get_news_count(db:AsyncSession,category_id:int):
    #查询的是指定分类下的新闻数量
    stmt=select(func.count(News.id)).where(News.category_id == category_id)
    result=await db.execute(stmt)
    return result.scalar_one()#只能有一个结果否则报错
async def get_news_detail(db:AsyncSession,news_id:int):
    stmt=select(News).where(News.id == news_id)
    result=await db.execute(stmt)
    return result.scalar_one_or_none()




