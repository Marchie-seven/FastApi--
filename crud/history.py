from datetime import datetime
from pydoc import pager
from sqlalchemy import select, func,delete
from config.db_conf import AsyncSession
from models.history import History
from models.news import News
from models.users import User


async def add_history(news_id: int,user: User, db: AsyncSession,):
    stmt= select(History).where(History.news_id==news_id).where(History.user_id==user.id)
    result=await db.execute(stmt)
    existing_history = result.scalar_one_or_none()
    if existing_history is None:
        history = History(news_id=news_id,user_id=user.id)
        db.add(history)
        await db.commit()
        await db.refresh(history)
        return history
    else:
        existing_history.view_time = datetime.now()
        await db.commit()
        await db.refresh(existing_history)
        return existing_history

async def get_history(user: User
                      ,db: AsyncSession,
                      page: int = 1,
                      page_size: int = 10,
                      ):
    total=select(func.count()).where(History.user_id==user.id)
    get_total=await db.execute(total)
    totals=get_total.scalar_one_or_none()
    stmt=(select(News,History.view_time.label("viewtime"),History.id.label("historyid"))
          .join(History,News.id==History.news_id)
          .where(History.user_id==user.id)
          .order_by(History.id.desc())
          .offset((page-1)*page_size).limit(page_size))
    result=await db.execute(stmt)
    history=result.all()
    return history,totals

async def delete_history(history_id: int,user: User, db: AsyncSession):
    stmt=delete(History).where(History.id==history_id).where(History.user_id==user.id)
    await db.execute(stmt)
    await db.commit()
    return True

#清空浏览历史记录
async def clear_history(user: User, db: AsyncSession):
    stmt=delete(History).where(History.user_id==user.id)
    await db.execute(stmt)
    await db.commit()
    return True



























