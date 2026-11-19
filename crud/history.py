from datetime import datetime

from sqlalchemy import select
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































