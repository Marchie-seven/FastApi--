# 根据用户名查询数据库
import uuid
from datetime import timedelta, datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from sqlalchemy.sql.functions import user

from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest, UserChangeRequest
from utils import security

#根据用户名查询数据库
async def get_user_by_username(db: AsyncSession,username:str):
    query=select(User).where(User.username==username)
    result=await db.execute(query)
    return result.scalar_one_or_none()
# 创建用户
async def create_user(db: AsyncSession,user_data:UserRequest):
    #先密码加密处理->ad
    hashed_password=security.get_hash_password(user_data.password)
    user=User(username=user_data.username,password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)#从数据库读回最新的user
    return user

#生成Token
async def create_token(db: AsyncSession,user_id:int):
    #生成Token+设置过期时间->查询数据库当前用户是否有Token->有：更新：没有：添加
    token=str(uuid.uuid4())
    #timedelta(days=7,hours=2,minutes=30,seconds=10)
    expires_at=datetime.now()+timedelta(days=7)
    query=select(UserToken).where(UserToken.user_id==user_id)
    result=await db.execute(query)
    user_token=result.scalar_one_or_none()
    if user_token:
        user_token.token=token
        user_token.expires_at=expires_at
    else:
        user_token=UserToken(user_id=user_id,token=token,expires_at=expires_at)
        db.add(user_token)
        await db.commit()
    return token

async def authenticate_user(db: AsyncSession,username:str,password:str):
    user=await get_user_by_username(db,username)
    if not user:
        return None
    print("--- 正在进行登录校验 ---")
    print("用户输入的明文密码:", password)
    print("数据库中的加密密码:", user.password)
    is_match = security.verify_password(password, user.password)
    print("校验结果 (True/False):", is_match)

    if not is_match:
        return None
    return user

#根据Token查询用户:验证Token->查询用户
async def get_user_by_token(db: AsyncSession,token:str):
    query=select(UserToken).where(UserToken.token==token)
    result=await db.execute(query)
    db_token=result.scalar_one_or_none()
    if not db_token or db_token.expires_at < datetime.now():
        return None
    query=select(User).where(User.id==db_token.user_id)
    result=await db.execute(query)
    return result.scalar_one_or_none()

# 更新用户信息update更新->检查是否命中->获取更新后的用户信息->返回用户信息
async def update_user(db: AsyncSession,username:str,user_data:UserUpdateRequest):
    # update(User).where(User.username==username).value(字段=值，)
    # user_data是一个pydantic类型得到字典->**解包
    #没有设置值的不更新
    query=update(User).where(User.username==username).values(**user_data.model_dump(
        exclude_unset=True,
        exclude_none=True,
    ))
    result=await db.execute(query)
    await db.commit()
    #检查更新
    if result.rowcount==0:
        raise HTTPException(status_code=404,detail='用户不存在')
    #获取用户的信息
    update_user=await get_user_by_username(db,username)
    return update_user

#修改密码：验证旧密码->新密码加密->修改密码
async def change_password(db: AsyncSession,user:User,old_password:str,new_password:str):
    #验证旧密码
    if not security.verify_password(old_password,user.password):
        return False
    hash_newpassword=security.get_hash_password(new_password)
    user.password=hash_newpassword
    #更新：由sqlalchemy真正接管这个user对象确保可以commit
    #规避session过期或关闭导致不能提交的问题
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True






























